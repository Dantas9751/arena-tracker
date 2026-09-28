import re

import cv2
import mss
import numpy as np
import pytesseract
from thefuzz import fuzz, process

from .config import CARD_REGIONS, TESSERACT_LANG, VALID_ITEMS


def preprocess_image(img):
    # Aceita tanto BGRA (captura de tela via mss) quanto BGR (imagem carregada com cv2.imread)
    conversion = cv2.COLOR_BGRA2GRAY if img.shape[2] == 4 else cv2.COLOR_BGR2GRAY
    gray = cv2.cvtColor(img, conversion)
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

            custom_config = f'-l {TESSERACT_LANG} --oem 3 --psm 7'
            text = pytesseract.image_to_string(processed_img, config=custom_config).strip()

            text_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text).strip()

            if text_limpo and len(text_limpo) > 3:
                match, score = process.extractOne(text_limpo, VALID_ITEMS, scorer=fuzz.ratio)

                if score > 40:
                    print(f"[OCR Carta {i}] Leu: '{text_limpo}' -> Match: '{match}' (Confiança: {score}%)")

                if score >= 75:
                    valid_matches.append(match)

    return valid_matches
