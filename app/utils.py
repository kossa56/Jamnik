import time
from datetime import datetime

def get_timestamp():
    """Zwraca sformatowany timestamp"""
    return datetime.now().strftime("%H:%M:%S")

def format_log_message(message, msg_type="INFO"):
    """Formatuje wiadomość dla logów"""
    return f"[{get_timestamp()}] [{msg_type}] {message}"

def validate_ip_address(ip):
    """Walidacja adresu IP"""
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
    return True

def validate_port(port):
    """Walidacja numeru portu"""
    try:
        port_num = int(port)
        return 1 <= port_num <= 65535
    except ValueError:
        return False

def calculate_fps(start_time, frame_count):
    """Obliczanie FPS"""
    elapsed = time.time() - start_time
    if elapsed > 0:
        return frame_count / elapsed
    return 0
