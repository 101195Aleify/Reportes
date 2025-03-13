from database.connection import get_connection

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
