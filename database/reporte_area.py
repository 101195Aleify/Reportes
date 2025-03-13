from database.connection import get_connection
import pyodbc

def add_reporte_area(fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area, tanque_ap1, tanque_ap2, tanque_ap3, 
                     orden_del_area, identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO reporte_area (
                fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area, tanque_ap1, tanque_ap2, tanque_ap3, 
                orden_del_area, identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 

            (fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area, tanque_ap1, tanque_ap2, tanque_ap3, 
              orden_del_area, identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones))
        
        print(f"Guardado en reporte_area: fecha={fecha}, hora={hora}, producto={producto}, lote={lote}, "
              f"lugar_fabricacion_y_tanque_de_fabricacion={lugar_fabricacion_y_tanque_de_fabricacion}, "
              f"limpieza_area={limpieza_area}, tanque_ap1={tanque_ap1}, tanque_ap2={tanque_ap2}, "
              f"tanque_ap3={tanque_ap3} "
              f"orden_del_area={orden_del_area}, identificacion_tanque_agua_proceso={identificacion_tanque_agua_proceso}, "
              f"inspector_calidad={inspector_calidad}, ordenes_de_fabricacion={ordenes_de_fabricacion}, "
              f"observaciones={observaciones}")
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error al guardar en reporte_area: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

def get_reportes_area():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT id, fecha, hora, producto, lote, lugar_fabricacion_y_tanque_de_fabricacion, limpieza_area, 
                   tanque_ap1, tanque_ap2, tanque_ap3, orden_del_area, 
                   identificacion_tanque_agua_proceso, inspector_calidad, ordenes_de_fabricacion, observaciones 
            FROM reporte_area
        ''')
        reportes = cursor.fetchall()
        for reporte in reportes:
            print(f"Reporte de área cargado: {reporte}")
        print("Datos obtenidos de reporte_area:", reportes)
        return reportes
    except pyodbc.Error as e:
        print(f"Error al obtener reportes_area: {str(e)}")
        raise
    finally:
        conn.close()

def delete_reporte_area(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reporte_area WHERE id = ?", (id,))
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error al eliminar reporte_area: {str(e)}")
        raise
    finally:
        conn.close()