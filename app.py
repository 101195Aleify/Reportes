<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import threading
import time
from database import get_reviews, get_productos, add_review, delete_review, get_productos_relacionados, get_inspector
from localtunnel import start_localtunnel
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report  # Importar la nueva función
import pyodbc  # Importar pyodbc para la conexión a la base de datos

app = Flask(__name__)

@app.route('/')
def index():
    reviews = get_reviews()
    productos = get_productos()
    productos_relacionados = []
    inspectores = get_inspector()
    print("Inspectores pasados al template:", inspectores)
    return render_template('index.html', reviews=reviews, productos=productos, productos_relacionados=productos_relacionados, inspectores=inspectores)

@app.route('/add', methods=['POST'])
def add_review_route():
    try:
        fecha = request.form['fecha']
        hora = request.form['hora']
        producto = request.form['producto']
        tipo_crema = request.form.get('tipo_crema')
        lote = request.form['lote']
        odp = request.form['odp']
        inspector = request.form.get('inspector_de_calidad', '')
        observaciones = request.form.get('observaciones', '')
        
        if tipo_crema:
            producto = f'{producto} - {tipo_crema}'
        
        etiquetas_de_identificacion = '1' if request.form.get('etiquetas_de_identificacion') == '1' else '0'
        materia_primas_identificadas = '1' if request.form.get('materia_primas_identificadas') == '1' else '0'
        limpieza_del_area = '1' if request.form.get('limpieza_del_area') == '1' else '0'
        orden_de_area = '1' if request.form.get('orden_de_area') == '1' else '0'
        limpieza_de_utensilitos = '1' if request.form.get('limpieza_de_utensilitos') == '1' else '0'
        orden_del_almacen = '1' if request.form.get('orden_del_almacen') == '1' else '0'
        
        print(f"Valores recibidos del formulario: {request.form}")
        print(f"Valores de checkboxes: etiquetas_de_identificacion={etiquetas_de_identificacion}, "
              f"materia_primas_identificadas={materia_primas_identificadas}, limpieza_del_area={limpieza_del_area}, "
              f"orden_de_area={orden_de_area}, limpieza_de_utensilitos={limpieza_de_utensilitos}, "
              f"orden_del_almacen={orden_del_almacen}")
        
        print(f"Producto combinado para guardar: {producto}")
        add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
                   limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones)
        return redirect('/')
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400

@app.route('/delete/<int:id>')
def delete_review_route(id):
    delete_review(id)
    return redirect(url_for('index'))

@app.route('/get_relacionados/<int:producto_id>')
def get_relacionados(producto_id):
    relacionados = get_productos_relacionados(producto_id)
    return jsonify(relacionados)

@app.route('/get_relacionados_nombre/<string:producto_nombre>')
def get_relacionados_nombre(producto_nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductoID FROM Producto WHERE Nombre = ?", (producto_nombre,))
    producto_id = cursor.fetchone()
    if producto_id:
        producto_id = producto_id[0]
        relacionados = get_productos_relacionados(producto_id)
        return jsonify(relacionados)
    else:
        return jsonify([])

@app.route('/download_pdf')
def download_pdf():
    # Obtener los datos de las revisiones
    reviews = get_reviews()
    # Generar el PDF usando la función importada
    pdf_buffer = generate_pdf_report(reviews)
    # Preparar el PDF para descarga
    return send_file(pdf_buffer, as_attachment=True, download_name="reporte_revisiones.pdf", mimetype='application/pdf')

@app.route('/download_excel')
def download_excel():
    # Obtener los datos de las revisiones
    reviews = get_reviews()
    # Generar el Excel usando la función importada
    excel_buffer = generate_excel_report(reviews)
    # Preparar el Excel para descarga
    return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_revisiones_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    port = 5000
    threading.Thread(target=lambda: app.run(debug=True, port=port, use_reloader=False)).start()
    time.sleep(3)
=======
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import threading
import time
from database import get_reviews, get_productos, add_review, delete_review, get_productos_relacionados, get_inspector
from localtunnel import start_localtunnel
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report  # Importar la nueva función
import pyodbc  # Importar pyodbc para la conexión a la base de datos

app = Flask(__name__)

@app.route('/')
def index():
    reviews = get_reviews()
    productos = get_productos()
    productos_relacionados = []
    inspectores = get_inspector()
    print("Inspectores pasados al template:", inspectores)
    return render_template('index.html', reviews=reviews, productos=productos, productos_relacionados=productos_relacionados, inspectores=inspectores)

@app.route('/add', methods=['POST'])
def add_review_route():
    try:
        fecha = request.form['fecha']
        hora = request.form['hora']
        producto = request.form['producto']
        tipo_crema = request.form.get('tipo_crema')
        lote = request.form['lote']
        odp = request.form['odp']
        inspector = request.form.get('inspector_de_calidad', '')
        observaciones = request.form.get('observaciones', '')
        
        if tipo_crema:
            producto = f'{producto} - {tipo_crema}'
        
        etiquetas_de_identificacion = '1' if request.form.get('etiquetas_de_identificacion') == '1' else '0'
        materia_primas_identificadas = '1' if request.form.get('materia_primas_identificadas') == '1' else '0'
        limpieza_del_area = '1' if request.form.get('limpieza_del_area') == '1' else '0'
        orden_de_area = '1' if request.form.get('orden_de_area') == '1' else '0'
        limpieza_de_utensilitos = '1' if request.form.get('limpieza_de_utensilitos') == '1' else '0'
        orden_del_almacen = '1' if request.form.get('orden_del_almacen') == '1' else '0'
        
        print(f"Valores recibidos del formulario: {request.form}")
        print(f"Valores de checkboxes: etiquetas_de_identificacion={etiquetas_de_identificacion}, "
              f"materia_primas_identificadas={materia_primas_identificadas}, limpieza_del_area={limpieza_del_area}, "
              f"orden_de_area={orden_de_area}, limpieza_de_utensilitos={limpieza_de_utensilitos}, "
              f"orden_del_almacen={orden_del_almacen}")
        
        print(f"Producto combinado para guardar: {producto}")
        add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
                   limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones)
        return redirect('/')
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400

@app.route('/delete/<int:id>')
def delete_review_route(id):
    delete_review(id)
    return redirect(url_for('index'))

@app.route('/get_relacionados/<int:producto_id>')
def get_relacionados(producto_id):
    relacionados = get_productos_relacionados(producto_id)
    return jsonify(relacionados)

@app.route('/get_relacionados_nombre/<string:producto_nombre>')
def get_relacionados_nombre(producto_nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductoID FROM Producto WHERE Nombre = ?", (producto_nombre,))
    producto_id = cursor.fetchone()
    if producto_id:
        producto_id = producto_id[0]
        relacionados = get_productos_relacionados(producto_id)
        return jsonify(relacionados)
    else:
        return jsonify([])

@app.route('/download_pdf')
def download_pdf():
    # Obtener los datos de las revisiones
    reviews = get_reviews()
    # Generar el PDF usando la función importada
    pdf_buffer = generate_pdf_report(reviews)
    # Preparar el PDF para descarga
    return send_file(pdf_buffer, as_attachment=True, download_name="reporte_revisiones.pdf", mimetype='application/pdf')

@app.route('/download_excel')
def download_excel():
    # Obtener los datos de las revisiones
    reviews = get_reviews()
    # Generar el Excel usando la función importada
    excel_buffer = generate_excel_report(reviews)
    # Preparar el Excel para descarga
    return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_revisiones_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    port = 5000
    threading.Thread(target=lambda: app.run(debug=True, port=port, use_reloader=False)).start()
    time.sleep(3)
>>>>>>> 1e8d6730b9d3458ad158bb847cedc0d045818701
    start_localtunnel(port)