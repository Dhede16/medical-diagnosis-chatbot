import hashlib
import mysql.connector
from mysql.connector import Error

#Konfigurasi Database
DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",        
    "port":     3306,
}
DB_NAME = "db_carebot_app"


#Helper 
def sha(text: str) -> str:
    """Hash string dengan SHA-256."""
    return hashlib.sha256(text.encode()).hexdigest()


def get_conn():
    """Kembalikan koneksi MySQL ke database DB_NAME."""
    return mysql.connector.connect(**DB_CONFIG, database=DB_NAME)


#Setup Database
def setup_database() -> tuple[bool, str]:
    """
    Buat database & tabel jika belum ada.
    Tambahkan akun demo (admin / admin123) bila belum ada.
    Return: (sukses: bool, pesan: str)
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cur  = conn.cursor()

        # Buat database
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cur.execute(f"USE {DB_NAME}")

        # Buat tabel users
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id         INT AUTO_INCREMENT PRIMARY KEY,
                username   VARCHAR(50) UNIQUE NOT NULL,
                password   VARCHAR(64) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Akun demo
        demo_pw = sha("admin123")
        cur.execute(
            "INSERT IGNORE INTO users (username, password) VALUES (%s, %s)",
            ("admin", demo_pw)
        )

        conn.commit()
        cur.close()
        conn.close()
        return True, "Database siap."

    except Error as e:
        return False, str(e)
