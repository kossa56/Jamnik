import cv2
from PIL import Image
import customtkinter as ctk
import time

class CameraStream:
    def __init__(self, app):
        self.app = app
        self.cap = None
        self.streaming = False
        self.last_frame_time = 0
        self.frame_count = 0
        self.fps_start_time = 0
        
    def start(self, stream_url, timeout=10):
        """Rozpoczęcie strumienia wideo z timeoutem"""
        try:
            self.app.log_to_terminal(f"Łączenie ze streamem: {stream_url}")
            self.update_status("Łączenie ze streamem...", "yellow")
            
            # Zwolnij poprzednią kamerę jeśli istnieje
            if self.cap is not None:
                self.cap.release()
                self.cap = None
            
            self.app.root.update_idletasks()
            
            # Próbuj połączyć się przez timeout sekund
            start_time = time.time()
            self.app.log_to_terminal("Próba połączenia ze streamem...")
            
            # Ustaw timeout dla OpenCV
            self.cap = cv2.VideoCapture(stream_url)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Mniejszy bufor
            
            # Spróbuj ustawić timeout odczytu
            self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            
            while not self.cap.isOpened() and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                self.app.log_to_terminal("Oczekiwanie na stream...")
                self.app.root.update_idletasks()
                # Próbuj ponownie
                self.cap = cv2.VideoCapture(stream_url)
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                self.cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
            
            if not self.cap.isOpened():
                raise Exception(f"Nie można połączyć się ze streamem w ciągu {timeout}s")
            
            # Sprawdź czy stream wysyła dane
            ret, frame = self.cap.read()
            if not ret:
                # Spróbuj jeszcze raz
                time.sleep(1)
                ret, frame = self.cap.read()
                
            if not ret:
                raise Exception("Stream połączony ale nie wysyła danych")
            
            self.streaming = True
            self.last_frame_time = time.time()
            self.fps_start_time = time.time()
            self.frame_count = 0
            
            self.update_status("Stream aktywny - odbieranie obrazu...", "green")
            self.app.log_to_terminal("✓ Stream video uruchomiony pomyślnie")
            
            # Rozpocznij aktualizację ramek
            self.update_frame()
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            self.update_status(f"Błąd streamu: {error_msg[:50]}", "red")
            self.app.log_to_terminal(f"✗ Błąd streamu: {error_msg}")
            
            if self.cap:
                self.cap.release()
                self.cap = None
                
            return False
    
    def update_status(self, message, color="white"):
        """Aktualizacja statusu przez główną aplikację"""
        self.app.update_status(message, color)
    
    def stop(self):
        """Zatrzymanie strumienia"""
        self.streaming = False
        if self.cap:
            self.cap.release()
            self.cap = None
            self.app.log_to_terminal("Stream video zatrzymany")
            self.update_status("Stream zatrzymany", "orange")
    
    def update_frame(self):
        """Aktualizacja ramki wideo"""
        if not self.streaming or self.cap is None:
            return
        
        try:
            ret, frame = self.cap.read()
            current_time = time.time()
            
            if ret:
                self.frame_count += 1
                
                # Oblicz FPS co sekundę
                elapsed = current_time - self.fps_start_time
                if elapsed >= 1.0:  # Co sekundę
                    fps = self.frame_count / elapsed if elapsed > 0 else 0
                    self.frame_count = 0
                    self.fps_start_time = current_time
                    
                    # Aktualizuj status z FPS
                    if fps > 0:
                        self.update_status(f"Stream: {int(fps)} FPS", "green")
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                
                # Określanie rozmiaru kontenera
                img_width, img_height = self.app.ui_manager.get_container_size()
                
                if img_width > 0 and img_height > 0:
                    # Użyj CTkImage zamiast PIL ImageTk.PhotoImage
                    ctk_image = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=(img_width, img_height)
                    )
                else:
                    # Domyślny rozmiar
                    ctk_image = ctk.CTkImage(
                        light_image=img,
                        dark_image=img,
                        size=(640, 480)
                    )
                
                # Aktualizacja UI
                self.app.ui_manager.update_video_frame(ctk_image, img.size)
                
                # Aktualizuj czas ostatniej ramki
                self.last_frame_time = current_time
                
            else:
                # Sprawdź czy stream się nie zawiesił
                if current_time - self.last_frame_time > 3:  # 3 sekundy bez ramki
                    self.app.log_to_terminal("Stream przerwany - brak danych")
                    self.update_status("Stream przerwany", "orange")
                    self.stop()
                return
                
        except cv2.error as e:
            # Błąd OpenCV - stream może być nieprawidłowy
            error_msg = str(e)
            self.app.log_to_terminal(f"Błąd OpenCV: {error_msg}")
            self.stop()
            return
            
        except Exception as e:
            error_msg = str(e)
            # Ignoruj błędy związane z zamknięciem aplikacji
            if "NoneType" not in error_msg and "invalid" not in error_msg:
                self.app.log_to_terminal(f"Błąd przetwarzania ramki: {error_msg}")
            
            self.stop()
            return
        
        # Kontynuacja aktualizacji (30 FPS ≈ 33ms)
        self.app.root.after(33, self.update_frame)