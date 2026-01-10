import customtkinter as ctk
import queue

from .ui_manager import UIManager
from .ssh_manager import SSHManager
from .camera_stream import CameraStream
from .control_handlers import ControlHandlers
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
        
        # Stan aplikacji
        self.stream_running = False
        self.ssh_queue = queue.Queue()
        
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
        # Aktualizuj też stream URL
        self.config['stream_port'] = 8554
    
    def get_ssh_manager(self):
        return self.ssh_manager
    
    def get_camera_stream(self):
        return self.camera_stream
    
    def get_control_handlers(self):
        return self.control_handlers
    
    def on_closing(self):
        """Zamykanie aplikacji"""
        self.ssh_manager.disconnect()
        self.camera_stream.stop()
        self.root.quit()