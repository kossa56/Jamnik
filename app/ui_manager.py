import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
from .config import COLORS, SIZES, KEY_MAPPINGS, TEXTS

class UIManager:
    def __init__(self, app):
        self.app = app
        self.root = app.root
        self.key_buttons = {}
        
        # Elementy UI
        self.image_label = None
        self.auto_image_label = None
        
        # Ramki trybów
        self.manual_frame = None
        self.auto_frame = None
        self.instructions_frame = None
        
        # Przyciski menu
        self.manual_btn = None
        self.auto_btn = None
        self.instructions_btn = None
        
    def setup_ui(self):
        """Konfiguracja całego interfejsu użytkownika"""
        self.setup_main_container()
        self.setup_sidebar()
        self.setup_content_frame()
        self.setup_config_frame()
        self.init_mode_frames()
        self.setup_terminal()
        self.setup_status_bar()
        self.setup_key_bindings()
        
        # Domyślnie pokaż tryb ręczny
        self.show_manual_control()
        
    def setup_main_container(self):
        """Główny kontener aplikacji"""
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
    def setup_sidebar(self):
        """Pasek boczny z menu"""
        self.sidebar = ctk.CTkFrame(
            self.main_container, 
            width=SIZES["sidebar_width"]
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 5), pady=10)
        self.sidebar.pack_propagate(False)
        
        # Nagłówek menu
        ctk.CTkLabel(
            self.sidebar, 
            text="Menu",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 30))
        
        # Przyciski menu
        self.create_menu_buttons()
        
    def create_menu_buttons(self):
        """Tworzenie przycisków menu"""
        self.manual_btn = ctk.CTkButton(
            self.sidebar,
            text="Sterowanie\nręczne",
            command=self.show_manual_control,
            height=50,
            font=("Arial", 14),
            corner_radius=8
        )
        self.manual_btn.pack(pady=8, padx=15, fill="x")
        
        self.auto_btn = ctk.CTkButton(
            self.sidebar,
            text="Sterowanie\nautomatyczne",
            command=self.show_auto_control,
            height=50,
            font=("Arial", 14),
            corner_radius=8
        )
        self.auto_btn.pack(pady=8, padx=15, fill="x")
        
        self.instructions_btn = ctk.CTkButton(
            self.sidebar,
            text="Instrukcja",
            command=self.show_instructions,
            height=50,
            font=("Arial", 14),
            corner_radius=8
        )
        self.instructions_btn.pack(pady=8, padx=15, fill="x")
        
        self.exit_btn = ctk.CTkButton(
            self.sidebar,
            text="Wyjście",
            command=self.app.on_closing,
            height=50,
            font=("Arial", 14),
            fg_color=COLORS["error"],
            hover_color=COLORS["error_hover"],
            corner_radius=8
        )
        self.exit_btn.pack(pady=8, padx=15, fill="x")
    
    def setup_content_frame(self):
        """Główna ramka zawartości"""
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.pack(side="right", fill="both", expand=True, pady=10, padx=(0, 10))
        
        # Nagłówek
        self.header_label = ctk.CTkLabel(
            self.content_frame, 
            text=TEXTS['app_title'],
            font=("Arial", 20, "bold")
        )
        self.header_label.pack(pady=(10, 10))
    
    def setup_config_frame(self):
        """Ramka konfiguracyjna SSH"""
        self.config_frame = ctk.CTkFrame(self.content_frame)
        self.config_frame.pack(pady=5, padx=10, fill="x")
        
        # Pola konfiguracyjne
        config_grid = ctk.CTkFrame(self.config_frame)
        config_grid.pack(pady=5, padx=10)
        
        # Hostname
        ctk.CTkLabel(config_grid, text="Host:", width=60, anchor="w").grid(row=0, column=0, padx=2, pady=2)
        self.host_entry = ctk.CTkEntry(config_grid, width=120)
        self.host_entry.insert(0, self.app.config['hostname'])
        self.host_entry.grid(row=0, column=1, padx=2, pady=2)
        
        # Port
        ctk.CTkLabel(config_grid, text="Port:", width=60, anchor="w").grid(row=0, column=2, padx=2, pady=2)
        self.port_entry = ctk.CTkEntry(config_grid, width=60)
        self.port_entry.insert(0, str(self.app.config['port']))
        self.port_entry.grid(row=0, column=3, padx=2, pady=2)
        
        # Username
        ctk.CTkLabel(config_grid, text="User:", width=60, anchor="w").grid(row=1, column=0, padx=2, pady=2)
        self.user_entry = ctk.CTkEntry(config_grid, width=120)
        self.user_entry.insert(0, self.app.config['username'])
        self.user_entry.grid(row=1, column=1, padx=2, pady=2)
        
        # Password
        ctk.CTkLabel(config_grid, text="Hasło:", width=60, anchor="w").grid(row=1, column=2, padx=2, pady=2)
        self.pass_entry = ctk.CTkEntry(config_grid, width=120, show="*")
        self.pass_entry.insert(0, self.app.config['password'])
        self.pass_entry.grid(row=1, column=3, padx=2, pady=2)
        
        # Przyciski SSH
        self.ssh_button_frame = ctk.CTkFrame(self.config_frame)
        self.ssh_button_frame.pack(pady=5)
        
        self.connect_button = ctk.CTkButton(
            self.ssh_button_frame,
            text="Połącz SSH",
            command=self.connect_and_start_stream,
            width=150,
            height=30,
            font=("Arial", 11)
        )
        self.connect_button.pack(side="left", padx=2)
        
        self.disconnect_button = ctk.CTkButton(
            self.ssh_button_frame,
            text="Rozłącz",
            command=self.disconnect_ssh,
            width=150,
            height=30,
            font=("Arial", 11),
            fg_color=COLORS["error"],
            hover_color=COLORS["error_hover"],
            state="disabled"
        )
        self.disconnect_button.pack(side="left", padx=2)
        
        # Główna ramka dla zawartości trybów
        self.mode_frame = ctk.CTkFrame(self.content_frame)
        self.mode_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Inicjalizacja trybów
        self.init_modes()
        
    def init_modes(self):
        """Inicjalizuj wszystkie tryby (jak w oryginalnym kodzie)"""
        # Tryb ręczny
        self.manual_frame = ctk.CTkFrame(self.mode_frame)
        
        # Kontener dla streamu i sterowania
        self.manual_container = ctk.CTkFrame(self.manual_frame)
        self.manual_container.pack(fill="both", expand=True, pady=5, padx=5)
        
        # Stream (70% szerokości)
        self.stream_frame = ctk.CTkFrame(self.manual_container, width=SIZES["stream_width"])
        self.stream_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.stream_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            self.stream_frame,
            text="Stream na żywo",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        # Ramka dla obrazu streamu
        self.image_container = ctk.CTkFrame(self.stream_frame)
        self.image_container.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Label do wyświetlania obrazu
        self.image_label = ctk.CTkLabel(self.image_container, text="Stream nieaktywny", fg_color="gray20")
        self.image_label.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Panel sterowania (30% szerokości)
        self.control_panel = ctk.CTkFrame(self.manual_container, width=SIZES["control_width"])
        self.control_panel.pack(side="right", fill="y", padx=(10, 0))
        self.control_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            self.control_panel,
            text="Sterowanie ręczne",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 20))
        
        # Sekcja sterowania kamerą
        cam_frame = ctk.CTkFrame(self.control_panel)
        cam_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            cam_frame,
            text="Sterowanie kamerą",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        cam_controls = ctk.CTkFrame(cam_frame)
        cam_controls.pack(pady=5)
        
        self.cam_left_btn = ctk.CTkButton(
            cam_controls,
            text="Q\nLewo",
            command=lambda: self.app.control_handlers.camera_left(),
            width=80,
            height=80,
            font=("Arial", 14, "bold"),
            corner_radius=10
        )
        self.cam_left_btn.pack(side="left", padx=5)
        
        self.cam_right_btn = ctk.CTkButton(
            cam_controls,
            text="E\nPrawo",
            command=lambda: self.app.control_handlers.camera_right(),
            width=80,
            height=80,
            font=("Arial", 14, "bold"),
            corner_radius=10
        )
        self.cam_right_btn.pack(side="left", padx=5)
        
        # Sekcja sterowania laserem
        laser_frame = ctk.CTkFrame(self.control_panel)
        laser_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            laser_frame,
            text="Sterowanie laserem",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        # Grid dla strzałek
        arrows_frame = ctk.CTkFrame(laser_frame)
        arrows_frame.pack(pady=10)
        
        # Rząd 1 (góra)
        self.up_btn = ctk.CTkButton(
            arrows_frame,
            text="↑",
            command=lambda: self.app.control_handlers.laser_up(),
            width=70,
            height=70,
            font=("Arial", 24, "bold"),
            corner_radius=10
        )
        self.up_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Rząd 2 (lewo, środek, prawo)
        self.left_btn = ctk.CTkButton(
            arrows_frame,
            text="←",
            command=lambda: self.app.control_handlers.laser_left(),
            width=70,
            height=70,
            font=("Arial", 24, "bold"),
            corner_radius=10
        )
        self.left_btn.grid(row=1, column=0, padx=5, pady=5)
        
        ctk.CTkLabel(
            arrows_frame,
            text="LASER",
            font=("Arial", 12, "bold")
        ).grid(row=1, column=1, padx=5, pady=5)
        
        self.right_btn = ctk.CTkButton(
            arrows_frame,
            text="→",
            command=lambda: self.app.control_handlers.laser_right(),
            width=70,
            height=70,
            font=("Arial", 24, "bold"),
            corner_radius=10
        )
        self.right_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # Rząd 3 (dół)
        self.down_btn = ctk.CTkButton(
            arrows_frame,
            text="↓",
            command=lambda: self.app.control_handlers.laser_down(),
            width=70,
            height=70,
            font=("Arial", 24, "bold"),
            corner_radius=10
        )
        self.down_btn.grid(row=2, column=1, padx=5, pady=5)
        
        # Mapowanie klawiszy do przycisków
        self.key_buttons = {
            'Q': self.cam_left_btn,
            'E': self.cam_right_btn,
            'UP': self.up_btn,
            'DOWN': self.down_btn,
            'LEFT': self.left_btn,
            'RIGHT': self.right_btn
        }
        
        # Tryb automatyczny
        self.auto_frame = ctk.CTkFrame(self.mode_frame)
        
        # Kontener dla streamu i informacji
        self.auto_container = ctk.CTkFrame(self.auto_frame)
        self.auto_container.pack(fill="both", expand=True, pady=5, padx=5)
        
        # Stream (70% szerokości) - TEN SAM STREAM CO W MANUAL!
        self.auto_stream_frame = ctk.CTkFrame(self.auto_container, width=SIZES["stream_width"])
        self.auto_stream_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.auto_stream_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            self.auto_stream_frame,
            text="Stream na żywo - Tryb automatyczny",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 5))
        
        # Ramka dla obrazu streamu - TEN SAM OBRAZ CO W MANUAL!
        self.auto_image_container = ctk.CTkFrame(self.auto_stream_frame)
        self.auto_image_container.pack(pady=5, padx=10, fill="both", expand=True)
        
        # Label do wyświetlania obrazu - TEN SAM LABEL CO W MANUAL!
        self.auto_image_label = ctk.CTkLabel(self.auto_image_container, text="Stream nieaktywny", fg_color="gray20")
        self.auto_image_label.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Panel informacji (30% szerokości)
        self.info_panel = ctk.CTkFrame(self.auto_container, width=SIZES["control_width"])
        self.info_panel.pack(side="right", fill="y", padx=(10, 0))
        self.info_panel.pack_propagate(False)
        
        ctk.CTkLabel(
            self.info_panel,
            text="Sterowanie automatyczne",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 20))
        
        # Informacje o programie
        info_text = ctk.CTkTextbox(self.info_panel, height=300)
        info_text.pack(pady=10, padx=15, fill="both", expand=True)
        info_text.insert("1.0",
            "Program: Śledzenie obiektów\n\n"
            "Status: Oczekiwanie...\n\n"
            "Parametry:\n"
            "• Tryb: Śledzenie ruchu\n"
            "• Czujnik: Kamera\n"
            "• Precyzja: Wysoka\n"
            "• Zakres: 360°\n\n"
            "Program automatycznie wykrywa\n"
            "i śledzi obiekty w polu widzenia."
        )
        info_text.configure(state="disabled", font=("Arial", 12))
        
        # Instrukcja
        self.instructions_frame = ctk.CTkFrame(self.mode_frame)
        
        ctk.CTkLabel(
            self.instructions_frame,
            text="Instrukcja obsługi",
            font=("Arial", 18, "bold")
        ).pack(pady=(20, 10))
        
        instructions_text = ctk.CTkTextbox(self.instructions_frame, height=400)
        instructions_text.pack(pady=20, padx=20, fill="both", expand=True)
        instructions_text.insert("1.0",
            "INSTRUKCJA OBSŁUGI\n\n"
            "1. KONFIGURACJA SSH:\n"
            "   • Wprowadź dane SSH do Raspberry Pi\n"
            "   • Kliknij 'Połącz SSH'\n\n"
            "2. STEROWANIE RĘCZNE:\n"
            "   • Strzałki (↑ ↓ ← →) - sterowanie laserem\n"
            "   • Q - obrót kamery w lewo\n"
            "   • E - obrót kamery w prawo\n"
            "   • Można używać przycisków lub klawiszy\n\n"
            "3. STEROWANIE AUTOMATYCZNE:\n"
            "   • Program automatycznie śledzi obiekty\n"
            "   • Wymaga aktywnego połączenia\n\n"
            "4. ROZWIĄZYWANIE PROBLEMÓW:\n"
            "   • Sprawdź połączenie sieciowe\n"
            "   • Sprawdź logi w terminalu"
        )
        instructions_text.configure(state="disabled", font=("Arial", 12))
    
    def init_mode_frames(self):
        """Inicjalizacja ramek trybów"""
        # Inicjalizacja już zrobiona w init_modes()
        pass
    
    def setup_terminal(self):
        """Terminal wyjściowy"""
        self.terminal_frame = ctk.CTkFrame(self.content_frame, height=SIZES["terminal_height"])
        self.terminal_frame.pack(pady=5, padx=10, fill="x")
        
        self.terminal_text = ctk.CTkTextbox(self.terminal_frame, height=70)
        self.terminal_text.pack(pady=(0, 5), padx=10, fill="both", expand=True)
        self.terminal_text.insert("1.0", TEXTS['terminal_welcome'])
        self.terminal_text.configure(state="disabled")
    
    def setup_status_bar(self):
        """Pasek statusu"""
        self.status_label = ctk.CTkLabel(
            self.content_frame,
            text=TEXTS['status_disconnected'],
            font=("Arial", 11)
        )
        self.status_label.pack(pady=(0, 5))
    
    def setup_key_bindings(self):
        """Konfiguracja wiązań klawiszy"""
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
    
    def on_key_press(self, event):
        """Obsługa naciśnięcia klawiszy"""
        key = event.keysym.upper()
        
        # Animacja przycisku
        if key in self.key_buttons:
            button = self.key_buttons[key]
            original_color = button.cget("fg_color")
            button.configure(fg_color=COLORS["primary_dark"])
            self.root.after(100, lambda: button.configure(fg_color=original_color))
        
        # Wywołanie odpowiedniej funkcji sterowania
        if key == 'UP':
            self.app.control_handlers.laser_up()
        elif key == 'DOWN':
            self.app.control_handlers.laser_down()
        elif key == 'LEFT':
            self.app.control_handlers.laser_left()
        elif key == 'RIGHT':
            self.app.control_handlers.laser_right()
        elif key == 'Q':
            self.app.control_handlers.camera_left()
        elif key == 'E':
            self.app.control_handlers.camera_right()
    
    def on_key_release(self, event):
        """Obsługa zwolnienia klawiszy"""
        key = event.keysym.upper()
        if key in self.key_buttons:
            # Przywróć oryginalny kolor - już obsłużone w animacji
            pass
    
    def show_manual_control(self):
        """Pokaż tryb ręcznego sterowania"""
        self.hide_all_frames()
        self.manual_frame.pack(fill="both", expand=True)
        self.manual_btn.configure(fg_color=COLORS["primary"])
        self.auto_btn.configure(fg_color=("gray75", "gray30"))
        self.instructions_btn.configure(fg_color=("gray75", "gray30"))
    
    def show_auto_control(self):
        """Pokaż tryb automatycznego sterowania"""
        self.hide_all_frames()
        self.auto_frame.pack(fill="both", expand=True)
        self.auto_btn.configure(fg_color=COLORS["primary"])
        self.manual_btn.configure(fg_color=("gray75", "gray30"))
        self.instructions_btn.configure(fg_color=("gray75", "gray30"))
    
    def show_instructions(self):
        """Pokaż instrukcję"""
        self.hide_all_frames()
        self.instructions_frame.pack(fill="both", expand=True)
        self.instructions_btn.configure(fg_color=COLORS["primary"])
        self.manual_btn.configure(fg_color=("gray75", "gray30"))
        self.auto_btn.configure(fg_color=("gray75", "gray30"))
    
    def hide_all_frames(self):
        """Ukryj wszystkie ramki trybów"""
        for frame in [self.manual_frame, self.auto_frame, self.instructions_frame]:
            frame.pack_forget()
    
    def animate_button_press(self, button):
        """Animacja kliknięcia przycisku"""
        original_color = button.cget("fg_color")
        button.configure(fg_color=COLORS["primary_dark"])
        
        # Przywróć oryginalny kolor po 100ms
        self.root.after(100, lambda: button.configure(fg_color=original_color))
    
    def log_to_terminal(self, message):
        """Dodawanie wiadomości do terminala"""
        self.root.after(0, self._update_terminal, message)
    
    def _update_terminal(self, message):
        """Aktualizacja terminala (wykonywane w głównym wątku)"""
        self.terminal_text.configure(state="normal")
        self.terminal_text.insert("end", f"{message}\n")
        self.terminal_text.see("end")
        self.terminal_text.configure(state="disabled")
    
    def update_status(self, message, color="white"):
        """Aktualizacja paska statusu"""
        self.root.after(0, self._update_status, message, color)
    
    def _update_status(self, message, color):
        """Aktualizacja statusu (wykonywane w głólnym wątku)"""
        self.status_label.configure(text=message, text_color=color)
    
    def update_video_frame(self, ctk_image, size):
        """Aktualizacja ramki wideo w UI - używa CTkImage"""
        if self.manual_frame.winfo_ismapped():
            # Ukryj tekst i pokaż obraz
            if self.image_label.cget("text") != "":
                self.image_label.configure(text="", image=ctk_image)
            else:
                self.image_label.configure(image=ctk_image)
            
            # Zapisz referencję do obrazu
            self.image_label.image_reference = ctk_image
        
        elif self.auto_frame.winfo_ismapped():
            # Ukryj tekst i pokaż obraz
            if self.auto_image_label.cget("text") != "":
                self.auto_image_label.configure(text="", image=ctk_image)
            else:
                self.auto_image_label.configure(image=ctk_image)
            
            # Zapisz referencję do obrazu
            self.auto_image_label.image_reference = ctk_image
        
        # Aktualizuj status z rozmiarem
        if hasattr(self, '_last_size') and self._last_size != size:
            self.update_status(f"Obraz: {size[0]}x{size[1]}", "green")
            self._last_size = size

    def clear_stream_labels(self):
        """Wyczyść etykiety streamu"""
        # Usuń referencje do obrazów
        if hasattr(self.image_label, 'image_reference'):
            self.image_label.image_reference = None
        
        if hasattr(self.auto_image_label, 'image_reference'):
            self.auto_image_label.image_reference = None
        
        # Ustaw tekst
        self.image_label.configure(image='', text="Stream nieaktywny")
        self.auto_image_label.configure(image='', text="Stream nieaktywny")
        
    def get_container_size(self):
        """Pobieranie rozmiaru kontenera obrazu"""
        if self.manual_frame.winfo_ismapped():
            if self.image_container.winfo_exists():
                img_width = self.image_container.winfo_width() - 20
                img_height = self.image_container.winfo_height() - 20
                return max(img_width, 100), max(img_height, 100)
        elif self.auto_frame.winfo_ismapped():
            if self.auto_image_container.winfo_exists():
                img_width = self.auto_image_container.winfo_width() - 20
                img_height = self.auto_image_container.winfo_height() - 20
                return max(img_width, 100), max(img_height, 100)
        return 640, 480
    
    def connect_and_start_stream(self):
        """Rozpoczęcie połączenia SSH i strumienia"""
        # Aktualizuj konfigurację z pól wejściowych
        self.app.update_config({
            'hostname': self.host_entry.get(),
            'port': int(self.port_entry.get()),
            'username': self.user_entry.get(),
            'password': self.pass_entry.get()
        })
        
        self.connect_button.configure(state="disabled", text="Łączenie...")
        self.update_status("Łączenie z Raspberry Pi via SSH...", "yellow")
        
        # Połącz SSH
        if self.app.ssh_manager.connect(self.app.config):
            # Uruchom strumień wideo
            stream_url = f"http://{self.app.config['hostname']}:{self.app.config['stream_port']}/stream"
            if self.app.camera_stream.start(stream_url):
                self.disconnect_button.configure(state="normal")
                self.connect_button.configure(text="Połączono", state="disabled")
            else:
                self.connect_button.configure(state="normal", text="Połącz SSH")
        else:
            self.connect_button.configure(state="normal", text="Połącz SSH")
    
    def disconnect_ssh(self):
        """Rozłączenie SSH"""
        self.app.ssh_manager.disconnect()
        self.app.camera_stream.stop()
        self.connect_button.configure(state="normal", text="Połącz SSH")
        self.disconnect_button.configure(state="disabled")
        self.update_status("Rozłączono z Raspberry Pi", "orange")
        
        # Zresetuj etykiety streamu
        self.image_label.configure(image='', text="Stream nieaktywny")
        self.auto_image_label.configure(image='', text="Stream nieaktywny")