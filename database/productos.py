from database.connection import get_connection

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
