import subprocess
import re
import time

def start_localtunnel(port):
    try:
        print(f"Iniciando LocalTunnel en el puerto {port}...")
        process = subprocess.Popen(f"npx localtunnel --port {port}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

        # Leer la salida en tiempo real para capturar la URL
        for line in iter(process.stdout.readline, ''):
            match = re.search(r"https://[a-zA-Z0-9-]+\.loca\.lt", line)
            if match:
                url = match.group(0)
                print(f"\n🔥 Tu aplicación está disponible en: {url}\n")
                break
        process.stdout.close()
    except Exception as e:
        print(f"Error iniciando LocalTunnel: {e}")