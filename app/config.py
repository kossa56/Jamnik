# Kolory aplikacji
COLORS = {
    "primary": "#3B8ED0",
    "primary_dark": "#1F6AA5",
    "secondary": "#2B2B2B",
    "error": "#D35B58",
    "error_hover": "#C23B38",
    "success": "#2E8B57",
    "warning": "#FFA500",
    "info": "#17A2B8",
    "gray_light": "gray75",
    "gray_dark": "gray30"
}

# Rozmiary i geometria
SIZES = {
    "window": "1200x750",
    "sidebar_width": 180,
    "stream_width": 700,
    "control_width": 300,
    "terminal_height": 80
}

# Konfiguracja domyślna
DEFAULT_CONFIG = {
    'hostname': '100.124.18.53',
    'port': 22,
    'username': 'jamnik',
    'password': 'J@mn!k',
    'stream_port': 8554
}

# Mapowanie klawiszy do akcji
KEY_MAPPINGS = {
    'UP': 'laser_up',
    'DOWN': 'laser_down',
    'LEFT': 'laser_left',
    'RIGHT': 'laser_right',
    'Q': 'camera_left',
    'E': 'camera_right'
}

# Komendy SSH
SSH_COMMANDS = {
    'start_stream': "rpicam-vid -t 0 --width 1280 --height 720 --framerate 25 --codec mjpeg --listen -o tcp://0.0.0.0:{port}",
    'stop_stream': "pkill -f rpicam-vid"
}

# Teksty interfejsu
TEXTS = {
    'app_title': "Projekt Grupowy - JAMNIK",
    'status_disconnected': "Niepołączono. Skonfiguruj SSH i kliknij 'Połącz'",
    'status_connecting': "Łączenie z Raspberry Pi via SSH...",
    'status_connected': "Połączono - odbieranie strumienia...",
    'terminal_welcome': ">>> Terminal output będzie pojawiał się tutaj\n",
    
    # Dodatkowe teksty
    'menu_manual': "Sterowanie\nręczne",
    'menu_auto': "Sterowanie\nautomatyczne",
    'menu_instructions': "Instrukcja",
    'menu_exit': "Wyjście",
    
    # Teksty streamu
    'stream_inactive': "Stream nieaktywny",
    'stream_manual': "Stream na żywo",
    'stream_auto': "Stream na żywo - Tryb automatyczny",
    
    # Teksty YOLO (dodane)
    'yolo_title': "Detekcja obiektów (YOLO)",
    'yolo_class': "Klasa:",
    'yolo_confidence': "Pewność:",
    'yolo_start': "Start Auto-Śledzenie",
    'yolo_stop': "Stop Śledzenie",
    'yolo_status_inactive': "Status: Nieaktywny",
    'yolo_status_active': "Śledzenie aktywne",
    'yolo_status_stopped': "Śledzenie zatrzymane"
}

# Klasy YOLO (dodane)
YOLO_CLASSES = ["Wszystkie", "person", "car", "cat", "dog", "bird", "bottle", "cell phone", "chair"]
