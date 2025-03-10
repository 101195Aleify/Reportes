import pyodbc
import os
from contextlib import contextmanager

# Definir la conexión con la base de datos de Azure
@contextmanager
def get_connection():
    try:
        # Obtener las credenciales desde variables de entorno
        server = os.getenv('DB_SERVER', 'administradordereportes.database.windows.net')
        database = os.getenv('DB_NAME', 'Reporte')
        username = os.getenv('DB_USER', 'adminreporte')
        password = os.getenv('DB_PASSWORD', 'S1st3m4s123*+')  # Esto se configurará en Azure
        driver = '{ODBC Driver 17 for SQL Server}'

        # Cadena de conexión
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        conn = pyodbc.connect(conn_str)
        yield conn
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
    finally:
        conn.close()

def get_reviews():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM reviews")
            reviews = cursor.fetchall()
            for review in reviews:
                print(f"Review cargada: {review}")
            print("Datos obtenidos de reviews:", reviews)
            return reviews
    except pyodbc.Error as e:
        print(f"Error al obtener reviews: {e}")
        return []

def get_productos():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ProductoID, Nombre FROM Producto")
            productos = cursor.fetchall()
            print("Productos obtenidos:", productos)
            return productos
    except pyodbc.Error as e:
        print(f"Error al obtener productos: {e}")
        return []

def get_productos_relacionados(producto_id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT NombreProductoRelacion 
                FROM ProductoRelaciones 
                WHERE ProductoID = ?
            """, (producto_id,))
            relacionados = [row[0] for row in cursor.fetchall()]
            print(f"Productos relacionados para ProductoID {producto_id}:", relacionados)
            return relacionados
    except pyodbc.Error as e:
        print(f"Error al obtener productos relacionados: {e}")
        return []

def get_inspector(inspector_id=None):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            if inspector_id is not None:
                cursor.execute("SELECT id, nombre FROM inspector WHERE id = ?", (inspector_id,))
                result = cursor.fetchone()
                print(f"Inspector obtenido para ID {inspector_id}:", result)
                return result
            else:
                cursor.execute("SELECT id, nombre FROM inspector")
                inspectores = cursor.fetchall()
                print("Inspectores obtenidos desde la base de datos:", inspectores)
                return inspectores
    except pyodbc.Error as e:
        print(f"Error al obtener inspectores: {e}")
        return [] if inspector_id is None else None

def add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
               limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reviews (fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas,
                                    limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector_de_calidad, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas,
                  limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones))
            print(f"Guardado en reviews: fecha={fecha}, hora={hora}, producto={producto}, lote={lote}, odp={odp}, "
                  f"etiquetas_de_identificacion={etiquetas_de_identificacion}, materia_primas_identificadas={materia_primas_identificadas}, "
                  f"limpieza_del_area={limpieza_del_area}, orden_de_area={orden_de_area}, "
                  f"limpieza_de_utensilitos={limpieza_de_utensilitos}, orden_del_almacen={orden_del_almacen}, "
                  f"inspector_de_calidad={inspector}, observaciones={observaciones}")
            conn.commit()
    except pyodbc.Error as e:
        print(f"Error al agregar review: {e}")
        raise

def delete_review(id):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reviews WHERE id = ?", (id,))
            conn.commit()
    except pyodbc.Error as e:
        print(f"Error al eliminar review: {e}")
        raise