import subprocess
import time

# Solicitar el puerto de la aplicación Flask
port = input("Ingrese el puerto donde está alojada la aplicación Flask (por ejemplo, 5000): ")

# Iniciar localtunnel
def start_localtunnel(port):
    print(f"Iniciando localtunnel en el puerto {port}...")
    process = subprocess.Popen(f'lt --port {port}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    
    # Esperar unos segundos para que localtunnel genere la URL
    time.sleep(5)
    
    # Leer la salida y encontrar la URL pública
    url = None
    for line in process.stdout:
        if "https://" in line:
            url = line.strip()
            break
    
    if url:
        print(f"Tu aplicación ahora es pública en: {url}")
    else:
        print("No se pudo obtener la URL de localtunnel.")

# Llamar a tu aplicación Flask desde el script
def run_flask():
    print("Ejecutando la aplicación Flask...")
    subprocess.Popen(['python', 'app.py'])

# Ejecutar tu aplicación Flask y luego iniciar localtunnel
run_flask()
time.sleep(2)  # Un pequeño retraso para asegurarse de que Flask haya iniciado correctamente
start_localtunnel(port)
