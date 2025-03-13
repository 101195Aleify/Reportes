from database.connection import get_connection

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
