import os
import sys
import time
import keyboard
import pyautogui
import random
import subprocess
from datetime import datetime, timedelta

TEMPO_PULO = 0.18
TEMPO_FORA = 0.55

if os.geteuid() != 0:
    print("O script precisa de acesso Root para usar o teclado físico.", flush=True)
    print("Por favor, digite sua senha do Linux Mint:", flush=True)
    os.execvp("sudo", ["sudo", "-E", sys.executable] + sys.argv)

tempo_inicio = time.time()

def log(mensagem):
    hora = datetime.now().strftime("%H:%M:%S")
    segundos_rodando = int(time.time() - tempo_inicio)
    tempo_afk = str(timedelta(seconds=segundos_rodando))
    print(f"[{hora} | AFK: {tempo_afk}] {mensagem}", flush=True)

def capturar_id_janela():
    log("Aguardando seleção... Clique na janela com a cruzinha (+)")
    try:
        wid = subprocess.check_output(['xdotool', 'selectwindow']).decode().strip()
        log(f"Janela capturada com sucesso! (ID travado: {wid})")
        return wid
    except subprocess.CalledProcessError:
        log("Seleção cancelada ou erro ao capturar a janela.")
        return None

def focar_janela(wid):
    subprocess.run(['xdotool', 'windowactivate', wid])
    time.sleep(1.0)
    pyautogui.click()
    time.sleep(0.5)

def rotina_esteira(wid):
    log("Entrando no loop da esteira...")
    while True:
        focar_janela(wid) 
        
        log("Ação: Pulo para fora da esteira (Espaço + A)")
        keyboard.press('space')
        keyboard.press('a')
        time.sleep(TEMPO_PULO)
        keyboard.release('a')
        keyboard.release('space')
        
        time.sleep(TEMPO_FORA)
        
        log("Ação: Pulo de volta para a esteira (Espaço + D)")
        keyboard.press('space')
        keyboard.press('d')
        time.sleep(TEMPO_PULO)
        keyboard.release('d')
        keyboard.release('space')
        
        pausa = random.randint(30, 60)
        log(f"Ciclo concluído. Pausando por {pausa} segundos.")
        print("-" * 55, flush=True)
        time.sleep(pausa)

print("=" * 55, flush=True)
log("Iniciando Macro Roblox AFK (Movimento Natural Lateral)")
print("=" * 55, flush=True)

wid_jogo = capturar_id_janela()

if wid_jogo:
    rotina_esteira(wid_jogo)
else:
    input("\nPressione ENTER para fechar o terminal...")
