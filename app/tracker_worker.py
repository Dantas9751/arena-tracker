import time

from .ocr import scan_cards
from .riot_api import is_game_running


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
