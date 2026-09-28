import requests
import urllib3

from .config import LIVE_API_URL

# Desativa avisos de certificado SSL da Riot API local
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def is_game_running():
    try:
        # Timeout ultra rápido de 0.5s para não prender a thread
        res = requests.get(LIVE_API_URL, timeout=0.5, verify=False)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False
