import pyodbc

# Definir la conexión con la base de datos de Azure
def get_connection():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=administradordereportes.database.windows.net;'
        r'DATABASE=Reporte;'
        r'UID=adminreporte;'
        r'PWD=S1st3m4s123*+'
    )
    conn = pyodbc.connect(conn_str)
    return conn

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

def get_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ProductoID, Nombre FROM Producto")
    productos = cursor.fetchall()
    print("Productos obtenidos:", productos)
    conn.close()
    return productos

def get_productos_relacionados(producto_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT NombreProductoRelacion 
        FROM ProductoRelaciones 
        WHERE ProductoID = ?
    """, (producto_id,))
    relacionados = [row[0] for row in cursor.fetchall()]
    print(f"Productos relacionados para ProductoID {producto_id}:", relacionados)
    conn.close()
    return relacionados

def get_inspector(inspector_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if inspector_id is not None:
        cursor.execute("SELECT id, nombre FROM inspector WHERE id = ?", (inspector_id,))
        result = cursor.fetchone()
        print(f"Inspector obtenido para ID {inspector_id}:", result)
        conn.close()
        return result
    else:
        cursor.execute("SELECT id, nombre FROM inspector")
        inspectores = cursor.fetchall()
        print("Inspectores obtenidos desde la base de datos:", inspectores)
        conn.close()
        return inspectores

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

# Funciones para el nuevo reporte
def get_nuevo_reportes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nuevo_reporte")
    reviews = cursor.fetchall()
    for review in reviews:
        print(f"Nuevo reporte cargado: {review}")
    print("Datos obtenidos de nuevo_reporte:", reviews)
    conn.close()
    return reviews

def add_nuevo_reporte(fecha, hora, producto, lote, sanitizante_en_turno, operadores_con_cubrebocas_y_guantes, 
                      pizarron_con_datos_del_producto, suelo_libre_de_pt, limpieza_de_componentes_opt, 
                      limpieza_de_area, limpieza_de_eutencilios, tarimas_limpias, inspector, observaciones):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nuevo_reporte (fecha, hora, producto, lote, sanitizante_en_turno, operadores_con_cubrebocas_y_guantes,
                                   pizarron_con_datos_del_producto, suelo_libre_de_pt, limpieza_de_componentes_opt,
                                   limpieza_de_area, limpieza_de_eutencilios, tarimas_limpias, inspector_de_calidad, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
        (fecha, hora, producto, lote, sanitizante_en_turno, operadores_con_cubrebocas_y_guantes,
         pizarron_con_datos_del_producto, suelo_libre_de_pt, limpieza_de_componentes_opt,
         limpieza_de_area, limpieza_de_eutencilios, tarimas_limpias, inspector, observaciones))
    print(f"Guardado en nuevo_reporte: fecha={fecha}, hora={hora}, producto={producto}, lote={lote}, "
          f"sanitizante_en_turno={sanitizante_en_turno}, operadores_con_cubrebocas_y_guantes={operadores_con_cubrebocas_y_guantes}, "
          f"pizarron_con_datos_del_producto={pizarron_con_datos_del_producto}, suelo_libre_de_pt={suelo_libre_de_pt}, "
          f"limpieza_de_componentes_opt={limpieza_de_componentes_opt}, limpieza_de_area={limpieza_de_area}, "
          f"limpieza_de_eutencilios={limpieza_de_eutencilios}, tarimas_limpias={tarimas_limpias}, "
          f"inspector_de_calidad={inspector}, observaciones={observaciones}")
    conn.commit()
    conn.close()

def delete_nuevo_reporte(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM nuevo_reporte WHERE id = ?", (id,))
    conn.commit()
    conn.close()