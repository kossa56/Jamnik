class ControlHandlers:
    def __init__(self, app):
        self.app = app
        
    def camera_left(self):
        self.app.log_to_terminal("Kamera: Obrót w lewo")
        self._send_control_command("CAM_LEFT")
        self._animate_button_manual('Q')
        
    def camera_right(self):
        self.app.log_to_terminal("Kamera: Obrót w prawo")
        self._send_control_command("CAM_RIGHT")
        self._animate_button_manual('E')
        
    def laser_up(self):
        self.app.log_to_terminal("Laser: Ruch w górę")
        self._send_control_command("LASER_UP")
        self._animate_button_manual('UP')
        
    def laser_down(self):
        self.app.log_to_terminal("Laser: Ruch w dół")
        self._send_control_command("LASER_DOWN")
        self._animate_button_manual('DOWN')
        
    def laser_left(self):
        self.app.log_to_terminal("Laser: Ruch w lewo")
        self._send_control_command("LASER_LEFT")
        self._animate_button_manual('LEFT')
        
    def laser_right(self):
        self.app.log_to_terminal("Laser: Ruch w prawo")
        self._send_control_command("LASER_RIGHT")
        self._animate_button_manual('RIGHT')
    
    def _send_control_command(self, command):
        """Wysłanie komendy sterującej do Raspberry Pi"""
        ssh_manager = self.app.get_ssh_manager()
        if ssh_manager and ssh_manager.is_connected:
            # Przykładowe komendy - dostosuj do swojego projektu
            command_map = {
                "CAM_LEFT": "echo 'CAM_LEFT' > /tmp/control_pipe",
                "CAM_RIGHT": "echo 'CAM_RIGHT' > /tmp/control_pipe",
                "LASER_UP": "echo 'LASER_UP' > /tmp/control_pipe",
                "LASER_DOWN": "echo 'LASER_DOWN' > /tmp/control_pipe",
                "LASER_LEFT": "echo 'LASER_LEFT' > /tmp/control_pipe",
                "LASER_RIGHT": "echo 'LASER_RIGHT' > /tmp/control_pipe"
            }
            
            if command in command_map:
                result = ssh_manager.execute_command(command_map[command])
                if result:
                    self.app.log_to_terminal(f"Odpowiedź: {result}")
        else:
            self.app.log_to_terminal(f"[SYMULACJA] Wysłano komendę: {command}")
    
    def _animate_button_manual(self, key):
        """Ręczna animacja przycisku (dla kliknięć myszą)"""
        ui = self.app.ui_manager
        if key in ui.key_buttons:
            ui.animate_button_press(ui.key_buttons[key])