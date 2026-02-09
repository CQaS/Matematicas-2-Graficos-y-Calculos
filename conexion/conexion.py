""" import mysql.connector


def get_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="hr_db"
    )
 """

import pyodbc


def get_conexion():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=hr;'
        'Trusted_Connection=yes;'
    )
