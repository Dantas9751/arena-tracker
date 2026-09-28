import os
import re
import sys

import cv2
import pytesseract
from thefuzz import fuzz, process

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from app.config import CARD_REGIONS_BASE, TESSERACT_CMD, TESSERACT_LANG, VALID_ITEMS  # noqa: E402
from app.ocr import preprocess_image  # noqa: E402

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

IMAGE_PATH = os.path.join(PROJECT_ROOT, "image.png")


def testar_imagem(caminho_imagem):
    print(f"Lendo a imagem: {caminho_imagem}\n")
    img = cv2.imread(caminho_imagem)

    if img is None:
        print("ERRO: Imagem não encontrada! Verifique o nome do arquivo.")
        return

    for i, region in enumerate(CARD_REGIONS_BASE, start=1):
        # Recorta a imagem baseada nas coordenadas (Y:Y+H, X:X+W)
        y, x = region["top"], region["left"]
        h, w = region["height"], region["width"]
        cropped = img[y:y + h, x:x + w]

        # Processa a imagem cortada
        processed_img = preprocess_image(cropped)

        # MOSTRA A IMAGEM NA TELA PRA VOCÊ VER O RECORTE
        cv2.imshow(f"Carta {i} Tratada", processed_img)

        # Faz o OCR
        custom_config = f'-l {TESSERACT_LANG} --oem 3 --psm 7'
        text = pytesseract.image_to_string(processed_img, config=custom_config).strip()
        text_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', text).strip()

        print(f"--- CARTA {i} ---")
        print(f"Texto Bruto do Tesseract: '{text}'")
        print(f"Texto Limpo: '{text_limpo}'")

        if len(text_limpo) > 3:
            match, score = process.extractOne(text_limpo, VALID_ITEMS, scorer=fuzz.ratio)
            print(f"Match Fuzzy: '{match}' (Confiança: {score}%)")
            if score >= 75:
                print(">> RESULTADO: ITEM APROVADO E SALVO!")
            else:
                print(">> RESULTADO: IGNORADO (Confiança baixa)")
        else:
            print(">> RESULTADO: IGNORADO (Texto muito curto ou vazio)")
        print("-" * 30)

    print("\nPressione qualquer tecla na janela das imagens para fechar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    testar_imagem(IMAGE_PATH)
