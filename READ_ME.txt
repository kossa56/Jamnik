STRUKTURA PROJEKTU
├── main.py # Główny plik uruchamiający aplikację
└── app/ # Folder z modułami aplikacji
	├── init.py # Inicjalizacja pakietu Python
	├── app.py # Główna klasa aplikacji - koordynator
	├── ui_manager.py # Zarządzanie interfejsem użytkownika
	├── ssh_manager.py # Połączenia SSH z Raspberry Pi
	├── camera_stream.py # Odbieranie i wyświetlanie strumienia wideo
	├── control_handlers.py # Obsługa komend sterujących
	├── config.py # Konfiguracja, stałe, kolory
	└── utils.py # Narzędzia pomocnicze (opcjonalne)

	OPIS PLIKÓW
main.py (plik główny)
CEL: Uruchomienie aplikacji
CO MOŻNA POPRAWIAĆ:

Ustawienia początkowe okna (rozmiar, tytuł)

Konfigurację motywu CustomTkinter

Obsługę błędów przy starcie aplikacji

	app/app.py (rdzeń aplikacji)
CEL: Koordynacja wszystkich komponentów
CO MOŻNA POPRAWIAĆ:

Logikę inicjalizacji komponentów

Komunikację między modułami

Zarządzanie stanem aplikacji

Dodawanie nowych funkcjonalności

	app/ui_manager.py (interfejs)
CEL: Tworzenie i zarządzanie interfejsem użytkownika
CO MOŻNA POPRAWIAĆ:

Layout i wygląd: Kolory, czcionki, rozmiary

Przyciski: Dodawanie nowych, zmiana zachowania

Strumień wideo: Sposób wyświetlania obrazu

Terminal: Formatowanie wiadomości

Menu boczne: Dodawanie nowych opcji

Animacje: Efekty wizualne przycisków

Responsywność: Dostosowanie do różnych rozmiarów okna

	app/ssh_manager.py (połączenia sieciowe)
CEL: Komunikacja z Raspberry Pi via SSH
CO MOŻNA POPRAWIAĆ:

Bezpieczeństwo: Uwierzytelnianie, szyfrowanie

Komendy SSH: Dodawanie nowych poleceń

Obsługa błędów: Lepsze komunikaty, automatyczne ponawianie

Wydajność: Optymalizacja transferu danych

Monitoring: Sprawdzanie stanu połączenia

Logowanie: Szczegółowe logi diagnostyczne

	app/camera_stream.py (strumień wideo)
CEL: Odbieranie i przetwarzanie obrazu z kamery
CO MOŻNA POPRAWIAĆ:

Codec wideo: Obsługa różnych formatów (H264, MJPEG)

Wydajność: Optymalizacja FPS, zużycie CPU

Rozmiar obrazu: Skalowanie, proporcje

Stabilność: Obsługa przerw w strumieniu

CTkImage: Konwersja obrazu dla CustomTkinter

Buffering: Zarządzanie buforami ramek

	app/control_handlers.py (sterowanie)
CEL: Obsługa komend sterujących kamerą i laserem
CO MOŻNA POPRAWIAĆ:

Nowe komendy: Dodawanie funkcji sterowania

Protokół komunikacji: Zmiana sposobu wysyłania komend

Zabezpieczenia: Walidacja komend

Kolejkowanie: Zarządzanie wieloma komendami

Feedback: Potwierdzenie wykonania komend

Makro: Sekwencje automatycznych komend

	app/config.py (konfiguracja)
CEL: Przechowywanie stałych i ustawień
CO MOŻNA POPRAWIAĆ:

Kolory: Paleta kolorów aplikacji

Rozmiary: Wymiary elementów UI

Domyślne ustawienia: IP, porty, loginy

Mapowanie klawiszy: Przypisanie klawiszy do akcji

Teksty: Komunikaty, etykiety, pomoc

Komendy SSH: Szablony poleceń

	app/utils.py (narzędzia)
CEL: Funkcje pomocnicze
CO MOŻNA POPRAWIAĆ:

Walidacja: Sprawdzanie poprawności danych

Formatowanie: Przekształcanie danych

Logowanie: Zaawansowane funkcje logów

Konwersje: Transformacje obrazów, danych

Czas: Operacje timestamp, timing
