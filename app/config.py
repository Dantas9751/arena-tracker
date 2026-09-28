import mss

from .languages import get_tesseract_lang, get_valid_items

# -----------------------------------------------------------------------------
# TESSERACT
# -----------------------------------------------------------------------------
TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
TESSERACT_LANG = get_tesseract_lang()

# -----------------------------------------------------------------------------
# RIOT LIVE CLIENT DATA API
# -----------------------------------------------------------------------------
LIVE_API_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"

# -----------------------------------------------------------------------------
# REGIÕES DAS CARTAS NA TELA
# -----------------------------------------------------------------------------
# Coordenadas calibradas em 1920x1080. São escaladas em runtime (ver
# get_scaled_card_regions) para funcionar em qualquer resolução 16:9.
REFERENCE_RESOLUTION = (1920, 1080)

CARD_REGIONS_BASE = [
    {"top": 410, "left": 471, "width": 268, "height": 35},  # Carta 1
    {"top": 411, "left": 832, "width": 265, "height": 37},  # Carta 2
    {"top": 414, "left": 1181, "width": 268, "height": 34}  # Carta 3
]


def get_scaled_card_regions():
    with mss.mss() as sct:
        monitor = sct.monitors[1]

    scale_x = monitor["width"] / REFERENCE_RESOLUTION[0]
    scale_y = monitor["height"] / REFERENCE_RESOLUTION[1]

    aspect_ref = REFERENCE_RESOLUTION[0] / REFERENCE_RESOLUTION[1]
    aspect_actual = monitor["width"] / monitor["height"]
    if abs(aspect_actual - aspect_ref) > 0.05:
        print(f"[AVISO] Resolução {monitor['width']}x{monitor['height']} não é 16:9. "
              f"As coordenadas das cartas podem ficar desalinhadas (recalibre com tools/coord.py se necessário).")

    print(f"[Config] Resolução detectada: {monitor['width']}x{monitor['height']} "
          f"(referência: {REFERENCE_RESOLUTION[0]}x{REFERENCE_RESOLUTION[1]})")

    return [
        {
            "top": round(r["top"] * scale_y),
            "left": round(r["left"] * scale_x),
            "width": round(r["width"] * scale_x),
            "height": round(r["height"] * scale_y),
        }
        for r in CARD_REGIONS_BASE
    ]


CARD_REGIONS = get_scaled_card_regions()

# -----------------------------------------------------------------------------
# ITENS PRISMÁTICOS CONHECIDOS
# -----------------------------------------------------------------------------
# Lista bilíngue (PT-BR / EN-US) definida em languages.py. VALID_ITEMS usa o
# idioma selecionado em languages.LANGUAGE.
VALID_ITEMS = get_valid_items()
