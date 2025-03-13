from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file
import time
from database import (
    get_reviews, get_productos, add_review, delete_review, get_productos_relacionados, get_inspector, get_connection
)
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report

index_bp = Blueprint('index', __name__)

@index_bp.route('/index')
def index():
    reviews = get_reviews()
    productos = get_productos()
    productos_relacionados = []
    inspectores = get_inspector()
    print("Inspectores pasados al template:", inspectores)
    return render_template('index.html', reviews=reviews, productos=productos, productos_relacionados=productos_relacionados, inspectores=inspectores)

@index_bp.route('/add', methods=['POST'])
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
        add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
                   limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones)
        return redirect(url_for('index.index'))
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400

@index_bp.route('/delete/<int:id>')
def delete_review_route(id):
    delete_review(id)
    return redirect(url_for('index.index'))

@index_bp.route('/get_relacionados/<int:producto_id>')
def get_relacionados(producto_id):
    relacionados = get_productos_relacionados(producto_id)
    return jsonify(relacionados)

@index_bp.route('/get_relacionados_nombre/<string:producto_nombre>')
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

@index_bp.route('/download_pdf')
def download_pdf():
    reviews = get_reviews()
    pdf_buffer = generate_pdf_report(reviews)
    return send_file(pdf_buffer, as_attachment=True, download_name="reporte_revisiones.pdf", mimetype='application/pdf')

@index_bp.route('/download_excel')
def download_excel():
    reviews = get_reviews()
    excel_buffer = generate_excel_report(reviews)
    return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_revisiones_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')