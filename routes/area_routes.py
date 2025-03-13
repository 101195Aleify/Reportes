from flask import Blueprint, render_template, request, redirect, url_for, send_file
import time
from database import get_reportes_area, add_reporte_area, delete_reporte_area, get_productos, get_inspector
from pdf_generator import generate_pdf_report
from excel_generator import generate_excel_report

area_bp = Blueprint('area', __name__)

@area_bp.route('/area')
def area():
    try:
        # Espera 16 columnas: [id, fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area, tanque_ap1, tanque_ap2, tanque_ap3, limpios_identificados, orden_limpieza_area, identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones]
        reviews = get_reportes_area()
        productos = get_productos()
        inspectores = get_inspector()
        print("Reviews obtenidos:", reviews)
        return render_template('reporte_area.html', reviews=reviews, productos=productos, inspectores=inspectores)
    except Exception as e:
        print(f"Error al cargar /area: {str(e)}")
        return f"Error al cargar la página: {str(e)}", 500

@area_bp.route('/add_reporte_area', methods=['POST'])
def add_reporte_area_route():
    try:
        # Obtener los valores del formulario con los nombres corregidos
        fecha = request.form['fecha']
        hora = request.form['hora']
        producto = request.form['producto']
        lote = request.form['lote']
        lugar_fabricacion_y_tanque_de_fabricacion = request.form['lugar_fabricacion_y_tanque_de_fabricacion']
        limpieza_area = request.form.get('limpieza_area', '')  # Texto opcional
        tanque_ap1 = '1' if request.form.get('tanque_ap1') == '1' else '0'  # Checkbox
        tanque_ap2 = '1' if request.form.get('tanque_ap2') == '1' else '0'  # Checkbox
        tanque_ap3 = '1' if request.form.get('tanque_ap3') == '1' else '0'  # Checkbox
        orden_del_area = '1' if request.form.get('orden_del_area') == '1' else '0'  # Checkbox
        identificacion_tanque_agua_proceso = '1' if request.form.get('identificacion_tanque_agua_proceso') == '1' else '0'  # Checkbox, nombre corregido
        inspector_calidad = request.form.get('inspector_calidad', '')  # Selección obligatoria
        ordenes_de_fabricacion = request.form.get('ordenes_de_fabricacion', '')  # Texto opcional
        observaciones = request.form.get('observaciones', '')  # Texto opcional

        print(f"Valores recibidos del formulario: {request.form}")
        
        # Llamar a la función add_reporte_area con todos los parámetros (15 en total)
        add_reporte_area(
            fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area,
            tanque_ap1, tanque_ap2, tanque_ap3, orden_del_area,
            identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones
        )
        return redirect(url_for('area.area'))
    except KeyError as e:
        print(f"Error en el formulario: Falta el campo {e}")
        return "Error: Faltan campos requeridos en el formulario", 400
    except Exception as e:
        print(f"Error al procesar /add_reporte_area: {str(e)}")
        return f"Error al agregar el reporte: {str(e)}", 500

@area_bp.route('/delete_reporte_area/<int:id>')
def delete_reporte_area_route(id):
    try:
        delete_reporte_area(id)
        return redirect(url_for('area.area'))
    except Exception as e:
        print(f"Error al eliminar reporte_area: {str(e)}")
        return f"Error al eliminar: {str(e)}", 500

@area_bp.route('/download_pdf_area')
def download_pdf_area():
    try:
        reviews = get_reportes_area()
        pdf_buffer = generate_pdf_report(reviews)
        return send_file(pdf_buffer, as_attachment=True, download_name="reporte_area.pdf", mimetype='application/pdf')
    except Exception as e:
        print(f"Error al generar PDF: {str(e)}")
        return f"Error al generar el PDF: {str(e)}", 500

@area_bp.route('/download_excel_area')
def download_excel_area():
    try:
        reviews = get_reportes_area()
        excel_buffer = generate_excel_report(reviews)
        return send_file(excel_buffer, as_attachment=True, download_name=f"reporte_area_{time.strftime('%Y%m%d_%H%M%S')}.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        print(f"Error al generar Excel: {str(e)}")
        return f"Error al generar el Excel: {str(e)}", 500