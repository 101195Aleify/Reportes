from flask import Blueprint, render_template, request, redirect, url_for, send_file
import time
from database import get_nuevo_reportes, add_nuevo_reporte, delete_nuevo_reporte, get_productos, get_inspector
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report

nuevo_reporte_bp = Blueprint('nuevo_reporte', __name__)

@nuevo_reporte_bp.route('/nuevo_reporte')
def nuevo_reporte():
    reviews = get_nuevo_reportes()
    productos = get_productos()
    inspectores = get_inspector()
    return render_template('nuevo_reporte.html', reviews=reviews, productos=productos, inspectores=inspectores)

@nuevo_reporte_bp.route('/add_nuevo_reporte', methods=['POST'])
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
        add_nuevo_reporte(fecha, hora, producto, lote, sanitizante_en_turno, operadores_con_cubrebocas_y_guantes, 
                          pizarron_con_datos_del_producto, suelo_libre_de_pt, limpieza_de_componentes_opt, 
                          limpieza_de_area, limpieza_de_eutencilios, tarimas_limpias, inspector, observaciones)
        return redirect(url_for('nuevo_reporte.nuevo_reporte'))
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400

@nuevo_reporte_bp.route('/delete_nuevo_reporte/<int:id>')
def delete_nuevo_reporte_route(id):
    delete_nuevo_reporte(id)
    return redirect(url_for('nuevo_reporte.nuevo_reporte'))

@nuevo_reporte_bp.route('/download_pdf_nuevo_reporte')
def download_pdf_nuevo_reporte():
    reviews = get_nuevo_reportes()
    pdf_buffer = generate_pdf_report(reviews)
    return send_file(pdf_buffer, as_attachment=True, download_name="reporte_nuevo_reporte.pdf", mimetype='application/pdf')

@nuevo_reporte_bp.route('/download_excel_nuevo_reporte')
def download_excel_nuevo_reporte():
    reviews = get_nuevo_reportes()
    excel_buffer = generate_excel_report(reviews)
    return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_nuevo_reporte_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')