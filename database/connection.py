import pyodbc

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
