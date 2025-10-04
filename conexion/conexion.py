import mysql.connector


def get_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hr_db"
    )
