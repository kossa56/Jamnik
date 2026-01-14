import customtkinter as ctk
import queue

from .ui_manager import UIManager
from .ssh_manager import SSHManager
from .camera_stream import CameraStream
from .control_handlers import ControlHandlers
from .object_detector import ObjectDetector
from .config import DEFAULT_CONFIG

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Projekt Grupowy - JAMNIK")
        self.root.geometry("1200x750")
        
        # Konfiguracja
        self.config = DEFAULT_CONFIG.copy()
        
        # Komponenty
        self.ssh_manager = SSHManager(self)
        self.ui_manager = UIManager(self)
        self.camera_stream = CameraStream(self)
        self.control_handlers = ControlHandlers(self)
        self.object_detector = ObjectDetector(self)
        
        # Stan aplikacji
        self.stream_running = False
        self.ssh_queue = queue.Queue()
        self.auto_tracking = False
        self.tracking_timer = None
        
        # Inicjalizacja UI
        self.ui_manager.setup_ui()
        
    # Metody dostępowe dla komponentów
    def log_to_terminal(self, message):
        self.ui_manager.log_to_terminal(message)
    
    def update_status(self, message, color="white"):
        self.ui_manager.update_status(message, color)
    
    def get_config(self):
        return self.config.copy()
    
    def update_config(self, new_config):
        self.config.update(new_config)
        self.config['stream_port'] = 8554
    
    def get_ssh_manager(self):
        return self.ssh_manager
    
    def get_camera_stream(self):
        return self.camera_stream
    
    def get_control_handlers(self):
        return self.control_handlers
    
    def get_object_detector(self):
        return self.object_detector
    
    def start_auto_tracking(self):
        """Rozpoczęcie automatycznego śledzenia"""
        if not hasattr(self.object_detector, 'model') or self.object_detector.model is None:
            self.log_to_terminal("Błąd: Model YOLO nie został załadowany")
            return False
        
        self.auto_tracking = True
        self.object_detector.tracking_enabled = True
        self.object_detector.start_detection()
        self.log_to_terminal("Automatyczne śledzenie uruchomione")
        
        # Uruchom timer do śledzenia
        self._start_tracking_loop()
        return True
    
    def stop_auto_tracking(self):
        """Zatrzymanie automatycznego śledzenia"""
        self.auto_tracking = False
        self.object_detector.tracking_enabled = False
        self.object_detector.stop_detection()
        
        if self.tracking_timer:
            self.root.after_cancel(self.tracking_timer)
            self.tracking_timer = None
        
        self.log_to_terminal("Automatyczne śledzenie zatrzymane")
    
    def _start_tracking_loop(self):
        """Główna pętla śledzenia"""
        if not self.auto_tracking:
            return
        
        try:
            # Sprawdź czy jest wykryty obiekt i wygeneruj komendę
            if hasattr(self.ui_manager, 'last_frame_size'):
                frame_width, frame_height = self.ui_manager.last_frame_size
                command = self.object_detector.get_tracking_command(frame_width, frame_height)
                
                if command:
                    # Wykonaj komendę sterowania
                    handlers = self.control_handlers
                    if command == "CAM_LEFT":
                        handlers.camera_left()
                    elif command == "CAM_RIGHT":
                        handlers.camera_right()
                    elif command == "LASER_UP":
                        handlers.laser_up()
                    elif command == "LASER_DOWN":
                        handlers.laser_down()
            
            # Kontynuuj pętlę co 200ms
            self.tracking_timer = self.root.after(200, self._start_tracking_loop)
            
        except Exception as e:
            self.log_to_terminal(f"Błąd pętli śledzenia: {str(e)}")
    
    def on_closing(self):
        """Zamykanie aplikacji"""
        self.stop_auto_tracking()
        self.ssh_manager.disconnect()
        self.camera_stream.stop()
        self.object_detector.stop_detection()
        self.root.quit()
