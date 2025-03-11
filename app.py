from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import threading
import time
from database import get_reviews, get_productos, add_review, delete_review, get_productos_relacionados, get_inspector, get_connection, add_nuevo_reporte, get_nuevo_reportes, delete_nuevo_reporte
from localtunnel import start_localtunnel
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report  # Importar la nueva función
import pyodbc  # Importar pyodbc para la conexión a la base de datos
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
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
        return redirect('/index')
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

# Nuevas rutas para el nuevo reporte
@app.route('/nuevo_reporte')
def nuevo_reporte():
    reviews = get_nuevo_reportes()
    productos = get_productos()
    inspectores = get_inspector()
    return render_template('nuevo_reporte.html', reviews=reviews, productos=productos, inspectores=inspectores)

@app.route('/add_nuevo_reporte', methods=['POST'])
def add_nuevo_reporte_route():
    try:
        fecha = request.form['fecha']
        hora = request.form['hora']
        producto = request.form['producto']
        lote = request.form['lote']
        sanitizante_en_turno = '1' if request.form.get('sanitizante_en_turno') == '1' else '0'
        operadores_con_cubrebocas_y_guantes = '1' if request.form.get('operadores_con_cubrebocas_y_guantes') == '1' else '0'
        pizarron_con_datos_del_producto = '1' if request.form.get('pizarron_con_datos_del_producto') == '1' else '0'
        suelo_libre_de_pt = '1' if request.form.get('suelo_libre_de_pt') == '1' else '0'
        limpieza_de_componentes_opt = '1' if request.form.get('limpieza_de_componentes_opt') == '1' else '0'
        limpieza_de_area = '1' if request.form.get('limpieza_de_area') == '1' else '0'
        limpieza_de_eutencilios = '1' if request.form.get('limpieza_de_eutencilios') == '1' else '0'
        tarimas_limpias = '1' if request.form.get('tarimas_limpias') == '1' else '0'
        inspector = request.form.get('inspector_de_calidad', '')
        observaciones = request.form.get('observaciones', '')
        
        print(f"Valores recibidos del formulario: {request.form}")
        print(f"Valores de checkboxes: sanitizante_en_turno={sanitizante_en_turno}, "
              f"operadores_con_cubrebocas_y_guantes={operadores_con_cubrebocas_y_guantes}, pizarron_con_datos_del_producto={pizarron_con_datos_del_producto}, "
              f"suelo_libre_de_pt={suelo_libre_de_pt}, limpieza_de_componentes_opt={limpieza_de_componentes_opt}, "
              f"limpieza_de_area={limpieza_de_area}, limpieza_de_eutencilios={limpieza_de_eutencilios}, "
              f"tarimas_limpias={tarimas_limpias}")
        
        add_nuevo_reporte(fecha, hora, producto, lote, sanitizante_en_turno, operadores_con_cubrebocas_y_guantes, 
                          pizarron_con_datos_del_producto, suelo_libre_de_pt, limpieza_de_componentes_opt, 
                          limpieza_de_area, limpieza_de_eutencilios, tarimas_limpias, inspector, observaciones)
        return redirect('/nuevo_reporte')
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400

@app.route('/delete_nuevo_reporte/<int:id>')
def delete_nuevo_reporte_route(id):
    delete_nuevo_reporte(id)
    return redirect(url_for('nuevo_reporte'))

@app.route('/download_pdf_nuevo_reporte')
def download_pdf_nuevo_reporte():
    # Obtener los datos de las revisiones
    reviews = get_nuevo_reportes()
    # Generar el PDF usando la función importada
    pdf_buffer = generate_pdf_report(reviews)
    # Preparar el PDF para descarga
    return send_file(pdf_buffer, as_attachment=True, download_name="reporte_nuevo_reporte.pdf", mimetype='application/pdf')

@app.route('/download_excel_nuevo_reporte')
def download_excel_nuevo_reporte():
    # Obtener los datos de las revisiones
    reviews = get_nuevo_reportes()
    # Generar el Excel usando la función importada
    excel_buffer = generate_excel_report(reviews)
    # Preparar el Excel para descarga
    return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_nuevo_reporte_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))