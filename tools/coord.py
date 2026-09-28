import os

import cv2

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_PATH = os.path.join(PROJECT_ROOT, "image.png")


def pegar_coordenadas_da_imagem(caminho_imagem):
    # Carrega a sua imagem
    img = cv2.imread(caminho_imagem)
    
    if img is None:
        print(f"ERRO: Não consegui abrir a imagem '{caminho_imagem}'. Verifique o nome/extensão.")
        return

    # FORÇA a imagem a ter exatamente 1920x1080 para o mapeamento não ter erro
    img = cv2.resize(img, (1920, 1080))

    print("\n" + "="*50)
    print("📍 RASTREADOR DE COORDENADAS (FULLSCREEN 1920x1080)")
    print("="*50)
    print("COMO USAR:")
    print("1. A imagem vai abrir ocupando a tela inteira.")
    print("2. Clique e arraste para desenhar o retângulo em volta do nome da carta.")
    print("3. Aperte ENTER (ou ESPAÇO) para confirmar a seleção.")
    print("4. Repita para as 3 cartas.")
    print("="*50 + "\n")

    coordenadas_salvas = []
    
    # Usamos o mesmo nome de janela para manter o fullscreen entre as seleções
    titulo_janela = "Seletor de Cartas (Aperte ENTER para confirmar)"

    for i in range(1, 4):
        # Configura a janela para Tela Cheia (Fullscreen) antes de chamar o seletor
        cv2.namedWindow(titulo_janela, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(titulo_janela, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        
        print(f"-> Selecionando a Carta {i}...")
        
        # Abre a ferramenta de seleção na janela que acabamos de colocar em tela cheia
        roi = cv2.selectROI(titulo_janela, img, showCrosshair=True, fromCenter=False)
        
        x, y, w, h = roi
        
        # Se a pessoa selecionou um tamanho válido (largura e altura > 0)
        if w > 0 and h > 0:
            linha_codigo = f'{{"top": {y}, "left": {x}, "width": {w}, "height": {h}}}'
            print(f"✔ Carta {i} mapeada: {linha_codigo}")
            coordenadas_salvas.append(linha_codigo)
        else:
            print(f"❌ Seleção da Carta {i} foi cancelada.")
            coordenadas_salvas.append(None)
            
    cv2.destroyAllWindows()

    print("\n" + "="*50)
    print("📋 COPIE E COLE ISSO NO SEU app.py DENTRO DE CARD_REGIONS:")
    print("="*50)
    for coord in coordenadas_salvas:
        if coord:
            print(f"    {coord},")
    print("="*50 + "\n")

if __name__ == "__main__":
    pegar_coordenadas_da_imagem(IMAGE_PATH)