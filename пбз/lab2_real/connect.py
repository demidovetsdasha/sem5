import pyodbc

def connect_to_db():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=localhost;'  
            'DATABASE=master;'  
            'Trusted_Connection=yes'  
        )

        print(conn)

        return conn
    except pyodbc.Error as err:
        print(f"Ошибка подключения к базе данных: {err}")
        return None

