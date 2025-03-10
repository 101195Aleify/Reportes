import pandas as pd
from io import BytesIO
import time

def generate_excel_report(reviews):
    """
    Genera un reporte en formato Excel con los datos de revisiones.

    Args:
        reviews (list): Lista de registros de revisiones obtenidos de la base de datos.

    Returns:
        io.BytesIO: Buffer con el archivo Excel generado.
    """
    # Verificar si hay datos
    if not reviews:
        data = {"Mensaje": ["No hay datos de revisiones disponibles"]}
    else:
        # Crear una lista de diccionarios con los encabezados y datos
        headers = [
            "Fecha de Revisión", "Hora", "Producto", "Lote", "ODP",
            "Etiquetas de Identificación", "Materia Primas Identificadas",
            "Limpieza del Área", "Orden de Área", "Limpieza de Utensilitos",
            "Orden del Almacén", "Inspector de Calidad", "Observaciones"
        ]
        data = []
        for review in reviews:
            row = {
                "Fecha de Revisión": str(review[1]),
                "Hora": str(review[2]),
                "Producto": str(review[3]),
                "Lote": str(review[4]),
                "ODP": str(review[5]),
                "Etiquetas de Identificación": '✓' if review[6] == 1 or review[6] == '1' else '✗',
                "Materia Primas Identificadas": '✓' if review[7] == 1 or review[7] == '1' else '✗',
                "Limpieza del Área": '✓' if review[8] == 1 or review[8] == '1' else '✗',
                "Orden de Área": '✓' if review[9] == 1 or review[9] == '1' else '✗',
                "Limpieza de Utensilitos": '✓' if review[10] == 1 or review[10] == '1' else '✗',
                "Orden del Almacén": '✓' if review[11] == 1 or review[11] == '1' else '✗',
                "Inspector de Calidad": str(review[12]) if review[12] else '',
                "Observaciones": str(review[13]) if review[13] else ''
            }
            data.append(row)

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Crear un buffer para el archivo Excel
    output = BytesIO()
    # Exportar el DataFrame a Excel con un nombre de hoja y estilo básico
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name=f'Reporte_{time.strftime("%Y%m%d_%H%M%S")}', index=False)
        # Opcional: Ajustar el ancho de las columnas automáticamente
        worksheet = writer.sheets[f'Reporte_{time.strftime("%Y%m%d_%H%M%S")}']
        for i, col in enumerate(df.columns):
            column_length = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.column_dimensions[chr(65 + i)].width = column_length

    # Posicionar el cursor al inicio del buffer
    output.seek(0)

    return output
