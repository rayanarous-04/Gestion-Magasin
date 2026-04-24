import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise ConnectionError(f"Impossible de se connecter à la base de données : {e}")


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
            return cursor.rowcount

    except Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Erreur base de données : {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
