import mysql.connector

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "toor"


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor",
    )