import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_deteksi_prestasi"
        )

        if connection.is_connected():
            print("Koneksi berhasil")
            return connection

    except Error as e:
        print("Koneksi database gagal:", e)
        return None

# memanggil fungsi
connect_db()