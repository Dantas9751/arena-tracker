import sys
import time
import cv2
import mss
import numpy as np
import pytesseract
import requests
import urllib3
import re
from threading import Thread
from thefuzz import process, fuzz
from pynput import keyboard

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSizeGrip
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QFont

# Desativa avisos de certificado SSL da Riot API local
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração do caminho do Tesseract OCR no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# -----------------------------------------------------------------------------
# 1. CONFIGURAÇÕES E LISTAS
# -----------------------------------------------------------------------------
CARD_REGIONS = [
    {"top": 410, "left": 471, "width": 268, "height": 35},  # Carta 1
    {"top": 411, "left": 832, "width": 265, "height": 37},  # Carta 2
    {"top": 414, "left": 1181, "width": 268, "height": 34}  # Carta 3
]

PRISMATIC_ITEMS = [
    "Manopla do Buraco Negro", "Capa do Piromante", "Coroa da Rainha Despedaçada",
    "Crueldade", "Garras de Aço Sombrio", "Decapitador", "Coroa do Rei Demônio",
    "Abraço Demoníaco", "Orbe da Detonação", "Lança de Diamante", "Coração do Dragão",
    "Lâmina do Crepúsculo de Draktharr", "Milagre de Eleisa", "Promessa Empírea",
    "Glacieterno", "Comecarne", "Força da Entropia", "Fulminação",
    "Força do Vendaval", "Lâmina do Apostador", "Placa Gargolítica", "Hemodrenário",
    "Debilitador", "Elmo Hemomante", "Companheiro Hexraio", "Medalhão Enervante",
    "Jitte Kinkou", "Bastão Eletrizante", "Espada da Miragem", "Lâmina Enfeitiçada Moonflair",
    "Colhedor Noturno", "Garra do Espreitador", "Titereiro", "Virtude Radiante",
    "Fenda Dimensional", "Colheita do Ceifador", "Regicídio", "Reverberação",
    "Criarrunas", "Presente Sanguinário", "Escudo de Rocha Fundida", "Espada do Divino",
    "Talismã da Ascensão", "Quimiotanque Turbo", "Limite do Crepúsculo", 
    "Armadura de Sangue do Suserano", "Armadura de Warmog"
]

VALID_ITEMS = sorted(list(set(PRISMATIC_ITEMS)))
LIVE_API_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

# -----------------------------------------------------------------------------
# 2. SINAIS E INTERFACE DO OVERLAY (PyQt6)
# -----------------------------------------------------------------------------
class AppSignals(QObject):
    show_overlay = pyqtSignal()
    hide_overlay = pyqtSignal()
    update_items = pyqtSignal(set)

class ArenaOverlay(QWidget):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        
        self.signals.show_overlay.connect(self.show)
        self.signals.hide_overlay.connect(self.hide)
        self.signals.update_items.connect(self.update_seen_items)
        
        self.old_pos = None
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(50, 50, 320, 250)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QFrame(self)
        self.container.setStyleSheet("""
            QFrame {
                background-color: rgba(15, 23, 42, 0.90);
                border: 2px solid #38bdf8;
                border-radius: 10px;
            }
        """)
        container_layout = QVBoxLayout(self.container)
        
        title = QLabel("PRISMÁTICOS JÁ VISTOS")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title.setStyleSheet("color: #38bdf8; padding-bottom: 5px; border: none;")
        
        self.label_items = QLabel("- (Nenhum item visto ainda)")
        self.label_items.setFont(QFont("Arial", 10))
        self.label_items.setStyleSheet("color: #f8fafc; border: none;")
        self.label_items.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        container_layout.addWidget(title)
        container_layout.addWidget(self.label_items)
        container_layout.addStretch()

        grip_layout = QHBoxLayout()
        grip_layout.setContentsMargins(0, 0, 0, 0)
        grip_layout.addStretch()
        
        size_grip = QSizeGrip(self.container)
        size_grip.setStyleSheet("background-color: transparent; border: none;")
        grip_layout.addWidget(size_grip, 0, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        
        container_layout.addLayout(grip_layout)
        main_layout.addWidget(self.container)
        
        self.hide()

    def update_seen_items(self, items_set):
        if not items_set:
            self.label_items.setText("- (Nenhum item visto ainda)")
            return
        
        formatted_list = "\n".join([f"• {item}" for item in sorted(items_set)])
        self.label_items.setText(formatted_list)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None


# -----------------------------------------------------------------------------
# 3. TRATAMENTO DE IMAGEM E ENGINE DE OCR
# -----------------------------------------------------------------------------
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
    inverted = cv2.bitwise_not(thresh)
    return inverted

def scan_cards():
    valid_matches = []
    
    with mss.mss() as sct:
        for i, region in enumerate(CARD_REGIONS, start=1):
            screenshot = sct.grab(region)
            img = np.array(screenshot)
            processed_img = preprocess_image(img)
            
            custom_config = r'-l por --oem 3 --psm 7'
            text = pytesseract.image_to_string(processed_img, config=custom_config).strip()
            
            text_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text).strip()
            
            if text_limpo and len(text_limpo) > 3:
                match, score = process.extractOne(text_limpo, VALID_ITEMS, scorer=fuzz.ratio)
                
                if score > 40:
                    print(f"[OCR Carta {i}] Leu: '{text_limpo}' -> Match: '{match}' (Confiança: {score}%)")
                
                if score >= 75:
                    valid_matches.append(match)
                    
    return valid_matches

# -----------------------------------------------------------------------------
# 4. WORKER DE BACKGROUND OTIMIZADO (TURBO)
# -----------------------------------------------------------------------------
def is_game_running():
    try:
        # Timeout ultra rápido de 0.5s para não prender a thread
        res = requests.get(LIVE_API_URL, timeout=0.5, verify=False)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False

def ocr_worker(signals):
    seen_items = set()
    in_game_previous = False
    game_active = False
    api_check_counter = 0

    while True:
        # Checa a API apenas a cada 30 loops (aprox a cada 3 segundos) para não travar o OCR
        if api_check_counter >= 30 or not game_active:
            game_active = is_game_running()
            api_check_counter = 0
            
        if game_active:
            api_check_counter += 1

        if game_active and not in_game_previous:
            print("[+] Partida iniciada! Resetando lista de vistos.")
            in_game_previous = True
            seen_items.clear()
            signals.update_items.emit(seen_items)
            
        elif not game_active and in_game_previous:
            print("[-] Partida encerrada.")
            in_game_previous = False
            
        if game_active:
            detected_items = scan_cards()
            new_item_added = False
            
            for item in detected_items:
                if item not in seen_items:
                    seen_items.add(item)
                    new_item_added = True
                    print(f"[✔ NOVO REGISTRADO]: {item}")
            
            if new_item_added:
                signals.update_items.emit(seen_items)
                
            # Sleep ultra-baixo para leitura quase em tempo real
            time.sleep(0.1)
        else:
            # Se não estiver no jogo, relaxa a CPU
            time.sleep(3.0)

# -----------------------------------------------------------------------------
# 5. ESCUTA TECLA TAB GLOBAL
# -----------------------------------------------------------------------------
def start_keyboard_listener(signals):
    def on_press(key):
        if key == keyboard.Key.tab:
            signals.show_overlay.emit()

    def on_release(key):
        if key == keyboard.Key.tab:
            signals.hide_overlay.emit()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

# -----------------------------------------------------------------------------
# 6. INICIALIZAÇÃO DA APLICAÇÃO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    signals = AppSignals()
    overlay = ArenaOverlay(signals)
    
    start_keyboard_listener(signals)
    
    worker_thread = Thread(target=ocr_worker, args=(signals,), daemon=True)
    worker_thread.start()
    
    print("\n=== ARENA TRACKER RODANDO (MODO TURBO ATIVADO) ===")
    print("• Mantenha o LoL em modo 'Sem Borda' (Borderless).")
    print("• Fique de olho neste terminal para ver o que o OCR está lendo.")
    print("• Segure TAB para visualizar o overlay.")
    print("• Pressione Ctrl+C no terminal para encerrar.\n")
    
    sys.exit(app.exec())