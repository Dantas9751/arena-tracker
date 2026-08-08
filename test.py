import cv2
import pytesseract
import re
from thefuzz import process, fuzz

# Configuração do caminho do Tesseract OCR no Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 1. COORDENADAS E LISTA
CARD_REGIONS = [
    {"top": 339, "left": 397, "width": 218, "height": 32},  # Carta 1
    {"top": 339, "left": 693, "width": 216, "height": 35},  # Carta 2
    {"top": 330, "left": 1005, "width": 193, "height": 41}  # Carta 3
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

# 2. FUNÇÃO DE TRATAMENTO
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 140, 255, cv2.THRESH_BINARY)
    inverted = cv2.bitwise_not(thresh)
    return inverted

# 3. CARREGAR E TESTAR A IMAGEM
def testar_imagem(caminho_imagem):
    print(f"Lendo a imagem: {caminho_imagem}\n")
    img = cv2.imread(caminho_imagem)
    
    if img is None:
        print("ERRO: Imagem não encontrada! Verifique o nome do arquivo.")
        return

    for i, region in enumerate(CARD_REGIONS, start=1):
        # Recorta a imagem baseada nas coordenadas (Y:Y+H, X:X+W)
        y, x = region["top"], region["left"]
        h, w = region["height"], region["width"]
        cropped = img[y:y+h, x:x+w]
        
        # Processa a imagem cortada
        processed_img = preprocess_image(cropped)
        
        # MOSTRA A IMAGEM NA TELA PRA VOCÊ VER O RECORTE
        cv2.imshow(f"Carta {i} Tratada", processed_img)
        
        # Faz o OCR
        custom_config = r'-l por --oem 3 --psm 7'
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
    # COLOQUE O NOME DO SEU ARQUIVO DE IMAGEM AQUI:
    testar_imagem("image.png")