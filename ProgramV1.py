import customtkinter as ctk
from app.app import CameraApp

if __name__ == "__main__":
    # Konfiguracja CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = CameraApp(root)
    
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()