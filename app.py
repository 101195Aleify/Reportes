from flask import Flask, render_template, send_file
import os
from routes.index_routes import index_bp
from routes.nuevo_reporte_routes import nuevo_reporte_bp
from routes.area_routes import area_bp

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración opcional: puedes mover esto a un archivo de configuración separado si crece
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False') == 'True'  # Habilitar modo debug si está en entorno

# Registrar blueprints (módulos de rutas)
app.register_blueprint(index_bp)
app.register_blueprint(nuevo_reporte_bp)
app.register_blueprint(area_bp)

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ejecución de la aplicación
if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))  # Puerto por defecto 8000
    host = '0.0.0.0'  # Escucha en todas las interfaces
    app.run(host=host, port=port)