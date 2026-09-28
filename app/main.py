import sys
from threading import Thread

import pytesseract
from PyQt6.QtWidgets import QApplication

from .config import TESSERACT_CMD
from .input_listener import start_keyboard_listener
from .overlay import ArenaOverlay, AppSignals
from .tracker_worker import ocr_worker

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

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
