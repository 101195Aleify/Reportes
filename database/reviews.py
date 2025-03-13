from database.connection import get_connection

def get_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    for review in reviews:
        print(f"Review cargada: {review}")
    print("Datos obtenidos de reviews:", reviews)
    conn.close()
    return reviews

def add_review(fecha, hora, producto, lote, odp, etiquetas_de_identificacion, materia_primas_identificadas, 
               limpieza_del_area, orden_de_area, limpieza_de_utensilitos, orden_del_almacen, inspector, observaciones):
    conn = get_connection()
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
    conn.close()

def delete_review(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews WHERE id = ?", (id,))
    conn.commit()
    conn.close()
