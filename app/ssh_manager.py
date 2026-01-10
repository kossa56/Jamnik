import paramiko
import threading
import time
from .config import SSH_COMMANDS

class SSHManager:
    def __init__(self, app):
        self.app = app
        self.ssh_client = None
        self.ssh_channel = None
        self.is_connected = False
        self.stream_thread = None
        
    def connect(self, config):
        """Nawiązanie połączenia SSH"""
        try:
            self.app.log_to_terminal(f"Łączenie SSH: {config['hostname']}:{config['port']}")
            self.app.log_to_terminal(f"Użytkownik: {config['username']}")
            
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Ustaw timeout
            self.ssh_client.connect(
                hostname=config['hostname'],
                port=config['port'],
                username=config['username'],
                password=config['password'],
                timeout=10,
                banner_timeout=10,
                auth_timeout=10
            )
            
            self.is_connected = True
            self.app.log_to_terminal("✓ Połączono z Raspberry Pi!")
            
            # Test połączenia
            try:
                stdin, stdout, stderr = self.ssh_client.exec_command("echo 'SSH Connection Test'")
                output = stdout.read().decode().strip()
                if output:
                    self.app.log_to_terminal(f"Test SSH: {output}")
            except:
                pass
            
            # Uruchom strumień wideo na Raspberry Pi
            self.start_video_stream(config['stream_port'])
            
            return True
            
        except paramiko.ssh_exception.AuthenticationException as e:
            error_msg = "Błąd autoryzacji SSH - sprawdź login/hasło"
            self.app.log_to_terminal(f"BŁĄD SSH: {error_msg}")
            self.app.log_to_terminal(f"Szczegóły: {str(e)}")
            return False
            
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            error_msg = "Nie można nawiązać połączenia - sprawdź adres IP i port"
            self.app.log_to_terminal(f"BŁĄD SSH: {error_msg}")
            return False
            
        except Exception as e:
            error_msg = str(e)
            self.app.log_to_terminal(f"BŁĄD SSH: {error_msg}")
            return False
    
    def disconnect(self):
        """Rozłączenie SSH"""
        # Zatrzymaj wątek strumienia
        if self.stream_thread and self.stream_thread.is_alive():
            self.stop_video_stream()
            time.sleep(0.5)
        
        # Zamknij kanał SSH
        if self.ssh_channel:
            try:
                if self.ssh_channel.recv_ready():
                    self.ssh_channel.close()
            except:
                pass
            self.ssh_channel = None
        
        # Zamknij klienta SSH
        if self.ssh_client:
            try:
                self.ssh_client.close()
            except:
                pass
            self.ssh_client = None
        
        self.is_connected = False
        self.app.log_to_terminal("Rozłączono SSH")
    
    def start_video_stream(self, stream_port):
        """Uruchomienie strumienia wideo na Raspberry Pi"""
        command = SSH_COMMANDS['start_stream'].format(port=stream_port)
        self.app.log_to_terminal("Uruchamianie streamu na Raspberry Pi...")
        self.app.log_to_terminal(f"Komenda: {command}")
        
        # Sprawdź czy rpicam-vid jest zainstalowany
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command("which rpicam-vid")
            output = stdout.read().decode().strip()
            if not output:
                self.app.log_to_terminal("UWAGA: rpicam-vid nie znaleziony. Sprawdź instalację.")
        except:
            pass
        
        # Uruchomienie w osobnym wątku
        self.stream_thread = threading.Thread(target=self._stream_worker, args=(command,))
        self.stream_thread.daemon = True
        self.stream_thread.start()
        
        # Poczekaj chwilę na uruchomienie streamu
        time.sleep(3)
        self.app.log_to_terminal("Stream uruchomiony na Raspberry Pi (port {})".format(stream_port))
        
        return True
    
    def stop_video_stream(self):
        """Zatrzymanie strumienia wideo na Raspberry Pi"""
        if self.ssh_client and self.is_connected:
            try:
                self.app.log_to_terminal("Zatrzymywanie strumienia na Raspberry Pi...")
                self.execute_command(SSH_COMMANDS['stop_stream'])
                time.sleep(1)
                self.app.log_to_terminal("Strumień zatrzymany")
            except Exception as e:
                self.app.log_to_terminal(f"Błąd zatrzymywania strumienia: {str(e)}")
    
    def _stream_worker(self, command):
        """Wątek obsługujący strumień"""
        try:
            self.ssh_channel = self.ssh_client.get_transport().open_session()
            self.ssh_channel.exec_command(command)
            
            # Poczekaj na pierwsze dane
            time.sleep(2)
            
            # Monitorowanie outputu
            import select
            while self.is_connected:
                if self.ssh_channel.recv_ready():
                    output = self.ssh_channel.recv(1024).decode('utf-8', errors='ignore')
                    if output:
                        self.app.log_to_terminal(f"RPi: {output.strip()}")
                
                if self.ssh_channel.exit_status_ready():
                    exit_status = self.ssh_channel.recv_exit_status()
                    self.app.log_to_terminal(f"Stream zakończony z kodem: {exit_status}")
                    break
                    
                time.sleep(1)  # Sprawdzaj co sekundę
                
        except Exception as e:
            if self.is_connected:  # Tylko loguj jeśli jeszcze połączony
                self.app.log_to_terminal(f"Błąd strumienia SSH: {str(e)}")
    
    def execute_command(self, command):
        """Wykonanie komendy na zdalnym hoście"""
        if not self.is_connected or not self.ssh_client:
            self.app.log_to_terminal("Błąd: Brak połączenia SSH")
            return None
        
        try:
            stdin, stdout, stderr = self.ssh_client.exec_command(command, timeout=5)
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            
            if error:
                self.app.log_to_terminal(f"Błąd komendy: {error}")
            
            if output:
                return output
            
            return None
            
        except Exception as e:
            self.app.log_to_terminal(f"Błąd wykonania komendy: {str(e)}")
            return None
    
    def send_control_command(self, command):
        """Wysłanie komendy sterującej"""
        if self.is_connected:
            self.app.log_to_terminal(f"Wysyłanie komendy: {command}")
            # Tutaj dodaj kod do wysyłania konkretnych komend do Raspberry Pi
            return True
        else:
            self.app.log_to_terminal("Brak połączenia - komenda niezrealizowana")
            return False