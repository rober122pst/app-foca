import subprocess
import time
import threading
from plyer import notification

monitorar = False

def programa_aberto(nome_programa):
    try:
        import sys
        if sys.platform == 'win32':
            output = subprocess.check_output(['tasklist'], text=True)
            return nome_programa.lower() in output.lower()
            
    except Exception as e:
        print(f"Erro ao verificar processos: {e}")
        return False

def monitorar_programa(intervalo=10):
    print(f"Monitorando o programa: notepad.exe")
    
    while True:
        if monitorar:
            if programa_aberto('notepad.exe'):
                print("Programa detectado! Enviando notificação...")
                
                notification.notify(
                    title="Programa em Execução",
                    message=f"O programa notepad.exe está aberto!",
                    app_name="Monitor de Programas",
                    timeout=10
                )
                
        time.sleep(intervalo)

threading.Thread(target=monitorar_programa, daemon=True).start()

import socketio

sio = socketio.Client()

@sio.on('focus_mode')
def on_focus_mode(data):
    print("Conectado")
    if data['start']:
        global monitorar
        monitorar = data['start']
        print(monitorar)
        print('Pomodoro começou! Monitorando programas...')
    else:
        print('Pomodoro finalizado. Parando monitoramento.')

sio.connect('http://localhost:3000')
sio.wait()
