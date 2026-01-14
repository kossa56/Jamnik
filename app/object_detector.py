import cv2
import numpy as np
import time
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import threading
import queue

class ObjectDetector:
    def __init__(self, app, model_path='yolov8n.pt'):
        """
        Inicjalizacja detektora obiektów YOLO
        """
        self.app = app
        self.model_path = model_path
        self.model = None
        self.detecting = False
        self.detection_thread = None
        self.frame_queue = queue.Queue(maxsize=2)
        self.result_queue = queue.Queue(maxsize=2)
        self.confidence_threshold = 0.5
        self.target_class = None  # None = wszystkie klasy
        self.tracking_enabled = False
        self.last_detection = None
        self.detection_count = 0
        
        # Załaduj model YOLO
        self.load_model()
        
    def load_model(self):
        """Ładowanie modelu YOLO"""
        try:
            self.app.log_to_terminal("Ładowanie modelu YOLO...")
            self.model = YOLO(self.model_path)
            self.app.log_to_terminal("✓ Model YOLO załadowany pomyślnie")
            return True
        except Exception as e:
            self.app.log_to_terminal(f"✗ Błąd ładowania modelu YOLO: {str(e)}")
            self.app.log_to_terminal("Upewnij się, że zainstalowałeś ultralytics: pip install ultralytics")
            return False
    
    def start_detection(self):
        """Uruchomienie detekcji obiektów"""
        if self.model is None:
            self.app.log_to_terminal("Błąd: Model YOLO nie został załadowany")
            return False
        
        self.detecting = True
        self.detection_thread = threading.Thread(target=self._detection_worker)
        self.detection_thread.daemon = True
        self.detection_thread.start()
        self.app.log_to_terminal("Detekcja obiektów uruchomiona")
        return True
    
    def stop_detection(self):
        """Zatrzymanie detekcji"""
        self.detecting = False
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join(timeout=2)
        self.app.log_to_terminal("Detekcja obiektów zatrzymana")
    
    def set_target_class(self, class_name):
        """Ustawienie klasy obiektów do śledzenia"""
        # Mapowanie nazw klas YOLO
        class_map = {
            'person': 0,
            'car': 2,
            'cat': 15,
            'dog': 16,
            'bird': 14,
            'bottle': 39,
            'cup': 41,
            'chair': 56,
            'cell phone': 67
        }
        
        if class_name.lower() in class_map:
            self.target_class = class_map[class_name.lower()]
            self.app.log_to_terminal(f"Ustawiono śledzenie: {class_name}")
            return True
        else:
            self.target_class = None
            self.app.log_to_terminal(f"Nieznana klasa: {class_name}. Śledzenie wszystkich obiektów.")
            return False
    
    def set_confidence(self, confidence):
        """Ustawienie progu pewności"""
        self.confidence_threshold = max(0.1, min(0.99, confidence))
        self.app.log_to_terminal(f"Próg pewności ustawiony na: {self.confidence_threshold}")
    
    def process_frame(self, frame):
        """Przetwarzanie pojedynczej ramki"""
        if not self.detecting or self.model is None:
            return frame, []
        
        try:
            # Prześlij ramkę do kolejki
            if not self.frame_queue.full():
                self.frame_queue.put(frame.copy())
            
            # Pobierz wyniki jeśli dostępne
            if not self.result_queue.empty():
                processed_frame, detections = self.result_queue.get()
                return processed_frame, detections
            
            return frame, []
            
        except Exception as e:
            self.app.log_to_terminal(f"Błąd przetwarzania ramki: {str(e)}")
            return frame, []
    
    def _detection_worker(self):
        """Wątek przetwarzający detekcję obiektów"""
        while self.detecting:
            try:
                if not self.frame_queue.empty():
                    frame = self.frame_queue.get(timeout=0.1)
                    
                    # Wykonaj detekcję YOLO
                    results = self.model(frame, verbose=False)
                    
                    # Przetwarzaj wyniki
                    detections = []
                    processed_frame = frame.copy()
                    
                    if len(results) > 0:
                        result = results[0]
                        
                        # Rysuj bounding boxes i etykiety
                        processed_frame = self._draw_detections(frame, result)
                        
                        # Ekstrahuj detekcje
                        boxes = result.boxes
                        if boxes is not None:
                            for box in boxes:
                                conf = float(box.conf[0])
                                if conf >= self.confidence_threshold:
                                    cls = int(box.cls[0])
                                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                                    
                                    # Sprawdź czy pasuje do klasy docelowej
                                    if self.target_class is None or cls == self.target_class:
                                        # Oblicz środek obiektu
                                        center_x = (x1 + x2) // 2
                                        center_y = (y1 + y2) // 2
                                        
                                        detections.append({
                                            'class': cls,
                                            'class_name': self.model.names[cls],
                                            'confidence': conf,
                                            'bbox': [x1, y1, x2, y2],
                                            'center': (center_x, center_y),
                                            'area': (x2 - x1) * (y2 - y1)
                                        })
                    
                    # Zapisz ostatnią detekcję
                    if detections:
                        self.last_detection = detections[0]  # Używamy pierwszego wykrytego obiektu
                        self.detection_count += 1
                    
                    # Umieść w kolejce wyników
                    if not self.result_queue.full():
                        self.result_queue.put((processed_frame, detections))
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.app.log_to_terminal(f"Błąd wątku detekcji: {str(e)}")
                time.sleep(0.1)
    
    def _draw_detections(self, frame, result):
        """Rysowanie bounding boxes i etykiet na ramce"""
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Prosta czcionka
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        boxes = result.boxes
        if boxes is not None:
            for box in boxes:
                conf = float(box.conf[0])
                if conf >= self.confidence_threshold:
                    cls = int(box.cls[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    # Kolor w zależności od klasy
                    color = self._get_class_color(cls)
                    
                    # Rysuj bounding box
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
                    
                    # Rysuj etykietę
                    label = f"{result.names[cls]} {conf:.2f}"
                    text_bbox = draw.textbbox((x1, y1 - 20), label, font=font)
                    draw.rectangle(text_bbox, fill=color)
                    draw.text((x1, y1 - 20), label, fill="white", font=font)
                    
                    # Rysuj środek obiektu
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    draw.ellipse([center_x-3, center_y-3, center_x+3, center_y+3], 
                                 fill="red", outline="white")
        
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    def _get_class_color(self, class_id):
        """Zwraca kolor dla danej klasy"""
        colors = [
            (255, 0, 0),    # Czerwony - osoba
            (0, 255, 0),    # Zielony - samochód
            (0, 0, 255),    # Niebieski - zwierzęta
            (255, 255, 0),  # Cyjan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Żółty
            (128, 0, 128),  # Fiolet
            (128, 128, 0),  # Oliwkowy
        ]
        return colors[class_id % len(colors)]
    
    def get_tracking_command(self, frame_width, frame_height):
        """Generuje komendę sterowania do śledzenia obiektu"""
        if not self.last_detection or not self.tracking_enabled:
            return None
        
        det = self.last_detection
        center_x, center_y = det['center']
        
        # Oblicz odchylenie od środka ekranu
        screen_center_x = frame_width // 2
        screen_center_y = frame_height // 2
        
        dx = center_x - screen_center_x
        dy = center_y - screen_center_y
        
        # Próg martwej strefy (5% szerokości/wysokości)
        dead_zone_x = frame_width * 0.05
        dead_zone_y = frame_height * 0.05
        
        command = None
        
        # Sprawdź czy obiekt jest w martwej strefie
        if abs(dx) > dead_zone_x or abs(dy) > dead_zone_y:
            # Określ kierunek ruchu
            if abs(dx) > abs(dy):  # Ruch poziomy dominujący
                if dx > 0:
                    command = "CAM_RIGHT"  # Obiekt na prawo - obróć kamerę w prawo
                else:
                    command = "CAM_LEFT"   # Obiekt na lewo - obróć kamerę w lewo
            else:  # Ruch pionowy dominujący
                if dy > 0:
                    command = "LASER_DOWN"  # Obiekt na dole - laser w dół
                else:
                    command = "LASER_UP"    # Obiekt na górze - laser w górę
        
        return command
    
    def get_detection_info(self):
        """Zwraca informacje o aktualnych detekcjach"""
        if not self.last_detection:
            return "Brak wykryć"
        
        det = self.last_detection
        return f"{det['class_name']} ({det['confidence']:.2f}) - {det['center']}"