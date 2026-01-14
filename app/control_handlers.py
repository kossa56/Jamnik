class ControlHandlers:
    def __init__(self, app):
        self.app = app
        
    def camera_left(self):
        """PAN w lewo (kanał 0)"""
        self.app.log_to_terminal("PAN-TILT: Kamera w lewo")
        self._send_pantilt_command("pan_left")
        self._animate_button_manual('Q')
        
    def camera_right(self):
        """PAN w prawo (kanał 0)"""
        self.app.log_to_terminal("PAN-TILT: Kamera w prawo")
        self._send_pantilt_command("pan_right")
        self._animate_button_manual('E')
        
    def laser_up(self):
        """TILT w górę (kanał 1)"""
        self.app.log_to_terminal("PAN-TILT: Laser w górę")
        self._send_pantilt_command("tilt_up")
        self._animate_button_manual('UP')
        
    def laser_down(self):
        """TILT w dół (kanał 1)"""
        self.app.log_to_terminal("PAN-TILT: Laser w dół")
        self._send_pantilt_command("tilt_down")
        self._animate_button_manual('DOWN')
        
    def laser_left(self):
        """PAN w lewo dla lasera (kanał 0)"""
        self.app.log_to_terminal("PAN-TILT: Laser w lewo")
        self._send_pantilt_command("pan_left")
        self._animate_button_manual('LEFT')
        
    def laser_right(self):
        """PAN w prawo dla lasera (kanał 0)"""
        self.app.log_to_terminal("PAN-TILT: Laser w prawo")
        self._send_pantilt_command("pan_right")
        self._animate_button_manual('RIGHT')
    
    def _send_pantilt_command(self, command):
        """Wysyła komendę do Pan-Tilt HAT na Raspberry Pi"""
        ssh_manager = self.app.get_ssh_manager()
        
        if ssh_manager and ssh_manager.is_connected:
            try:
                # Uruchom skrypt Python na Raspberry Pi
                ssh_command = f"python3 /home/jamnik/pan_tilt_control.py {command}"
                result = ssh_manager.execute_command(ssh_command)
                
                if result:
                    # Pokaż wynik w terminalu
                    lines = result.strip().split('\n')
                    if lines:
                        self.app.log_to_terminal(f"RPi: {lines[-1]}")
                    else:
                        self.app.log_to_terminal(f"Wykonano: {command}")
                else:
                    self.app.log_to_terminal(f"Wykonano: {command}")
                    
            except Exception as e:
                self.app.log_to_terminal(f"Błąd wysyłania komendy: {str(e)}")
        else:
            # Symulacja gdy brak połączenia
            self.app.log_to_terminal(f"[SYMULACJA] Pan-Tilt: {command}")
    
    def _animate_button_manual(self, key):
        """Animacja przycisku po kliknięciu myszą"""
        ui = self.app.ui_manager
        if key in ui.key_buttons:
            ui.animate_button_press(ui.key_buttons[key])
