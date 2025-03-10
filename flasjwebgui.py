from flask import Flask
from flaskwebgui import FlaskUI
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Servidor Flask funcionando correctamente!"

def run_flask():
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == '__main__':
    # Iniciar Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Esperar a que Flask inicie
    time.sleep(2)

    # Iniciar FlaskUI correctamente
    FlaskUI(server="flask", app=app, width=800, height=600).run()
