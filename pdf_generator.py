from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import io
from reportlab.lib.units import inch
import time

def generate_pdf_report(reviews):
    """
    Genera un reporte en PDF con los datos de revisiones en formato horizontal.

    Args:
        reviews (list): Lista de registros de revisiones obtenidos de la base de datos.

    Returns:
        io.BytesIO: Buffer con el PDF generado.
    """
    # Crear un buffer para el PDF
    buffer = io.BytesIO()
    # Usar orientación horizontal (landscape) con márgenes ajustados
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=15, leftMargin=15, topMargin=15, bottomMargin=15)
    elements = []

    # Título del PDF
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Reporte de Revisiones de Calidad", styles['Title']))
    elements.append(Paragraph(f"Generado el: {time.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))  # Espacio

    # Preparar datos para la tabla
    data = [
        [
            "Fecha de Revisión", "Hora", "Producto", "Lote", "ODP",
            "Etiquetas de Identificación", "Materia Primas Identificadas",
            "Limpieza del Área", "Orden de Área", "Limpieza de Utensilitos",
            "Orden del Almacén", "Inspector de Calidad", "Observaciones"
        ]
    ]

    # Convertir los datos de reviews a la tabla del PDF
    for review in reviews:
        data.append([
            str(review[1]),  # fecha
            str(review[2]),  # hora
            str(review[3]),  # producto
            str(review[4]),  # lote
            str(review[5]),  # odp
            '✓' if review[6] == 1 or review[6] == '1' else '✗',  # etiquetas_de_identificacion
            '✓' if review[7] == 1 or review[7] == '1' else '✗',  # materia_primas_identificadas
            '✓' if review[8] == 1 or review[8] == '1' else '✗',  # limpieza_del_area
            '✓' if review[9] == 1 or review[9] == '1' else '✗',  # orden_de_area
            '✓' if review[10] == 1 or review[10] == '1' else '✗',  # limpieza_de_utensilitos
            '✓' if review[11] == 1 or review[11] == '1' else '✗',  # orden_del_almacen
            str(review[12]) if review[12] else '',  # inspector_de_calidad
            str(review[13]) if review[13] else ''   # observaciones
        ])

    # Ajustar los anchos de las columnas para aprovechar el espacio horizontal
    # Aumentamos el ancho de "Producto" y "Observaciones" para evitar cortes
    table = Table(data, colWidths=[
        1.0*inch,  # Fecha de Revisión
        0.8*inch,  # Hora
        3.0*inch,  # Producto (aumentado para nombres largos)
        1.0*inch,  # Lote
        1.0*inch,  # ODP
        0.5*inch,  # Etiquetas de Identificación (vertical)
        0.5*inch,  # Materia Primas Identificadas (vertical)
        0.5*inch,  # Limpieza del Área (vertical)
        0.5*inch,  # Orden de Área (vertical)
        0.5*inch,  # Limpieza de Utensilitos (vertical)
        0.5*inch,  # Orden del Almacén (vertical)
        1.5*inch,  # Inspector de Calidad
        3.0*inch   # Observaciones (aumentado para notas largas)
    ])

    # Estilo de la tabla optimizado para orientación horizontal
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),  # Reducir tamaño de fuente de encabezados
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),  # Reducir padding para ahorrar espacio
        # Rotar los encabezados de las columnas específicas (índices 5 al 10) -90 grados (hacia arriba)
        ('ROTATE', (5, 0), (10, 0), -90),  # Rotar -90 grados para "Etiquetas de Identificación" hasta "Orden del Almacén"
        ('VALIGN', (5, 0), (10, 0), 'MIDDLE'),  # Ajustar alineación vertical para los encabezados rotados
        ('ALIGN', (5, 0), (10, 0), 'CENTER'),  # Centrar el texto rotado
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),  # Reducir tamaño de fuente de datos
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), 'CJK'),  # Permitir ajuste de texto largo
    ]))

    # Permitir que la tabla se divida en varias páginas
    table.hAlign = 'LEFT'
    elements.append(table)
    doc.build(elements)

    # Retornar el buffer para que la aplicación lo use
    buffer.seek(0)
    return buffer
