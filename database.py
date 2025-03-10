import sqlite3

def get_reviews():
    with sqlite3.connect('quality_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reviews")
        reviews = cursor.fetchall()
        for review in reviews:
            print(f"Review cargada: {review}")
        print("Datos obtenidos de reviews:", reviews)
        return reviews

def get_productos():
    with sqlite3.connect('quality_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ProductoID, Nombre FROM Producto")
        productos = cursor.fetchall()
        print("Productos obtenidos:", productos)
        return productos

def get_productos_relacionados(producto_id):
    with sqlite3.connect('quality_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT NombreProductoRelacion 
            FROM ProductoRelaciones 
            WHERE ProductoID = ?
        """, (producto_id,))
        relacionados = [row[0] for row in cursor.fetchall()]
        print(f"Productos relacionados para ProductoID {producto_id}:", relacionados)
        return relacionados

def get_inspector(inspector_id=None):
    with sqlite3.connect('quality_reviews.db') as conn:
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

def add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
               limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones):
    with sqlite3.connect('quality_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reviews (fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas,
                                limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector_de_calidad, observaciones)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas,
             limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones))
        print(f"Guardado en reviews: fecha={fecha}, hora={hora}, producto={producto}, lote={lote}, odp={odp}, "
              f"etiquetas_de_identificacion={etiquetas_de_identificacion}, materia_primas_identificadas={materia_primas_identificadas}, "
              f"limpieza_del_area={limpieza_del_area}, orden_de_area={orden_de_area}, "
              f"limpieza_de_utensilitos={limpieza_de_utensilitos}, orden_del_almacen={orden_del_almacen}, "
              f"inspector_de_calidad={inspector}, observaciones={observaciones}")
        conn.commit()

def delete_review(id):
    with sqlite3.connect('quality_reviews.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = ?", (id,))
        conn.commit()
