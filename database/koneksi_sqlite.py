import sqlite3
import os
import sys
from pathlib import Path

# ==========================================
# KONFIGURASI DATABASE LOKAL
# ==========================================

def get_db_path():
    """Mendapatkan path database yang benar untuk .py dan .exe"""
    
    if getattr(sys, 'frozen', False):
        #  Running sebagai .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running sebagai script Python
        base_path = os.path.abspath(".")
    
    # Buat folder data jika belum ada
    db_dir = os.path.join(base_path, "data")
    os.makedirs(db_dir, exist_ok=True)
    
    return os.path.join(db_dir, "prediksi_siswa.db")

# Path database
DB_PATH = get_db_path()

def connect_db():
    """Koneksi ke database SQLite"""
    try:
        # Pastikan folder data ada
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH, timeout=20)
        
        # HAPUS BARIS INI! 
        # conn.row_factory = sqlite3.Row
        
        return conn
    except Exception as e:
        print(f"Error koneksi database: {e}")
        return None

def init_db():
    """Inisialisasi database dengan semua tabel yang diperlukan"""
    conn = connect_db()
    if not conn:
        print("❌ Gagal koneksi ke database!")
        return False
    
    cursor = conn.cursor()
    
    # ========== TABEL USERS ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # ========== TABEL KELAS ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kelas (
            id_kelas INTEGER PRIMARY KEY AUTOINCREMENT,
            id_user INTEGER,
            nama_kelas TEXT NOT NULL,
            tahun_ajaran TEXT,
            semester TEXT,
            FOREIGN KEY (id_user) REFERENCES users(id_user)
        )
    """)
    
    # ========== TABEL SISWA ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS siswa (
            id_siswa INTEGER PRIMARY KEY AUTOINCREMENT,
            id_kelas INTEGER,
            nis TEXT UNIQUE,
            nama_siswa TEXT NOT NULL,
            jenis_kelamin TEXT,
            tanggal_lahir TEXT,
            alamat TEXT,
            FOREIGN KEY (id_kelas) REFERENCES kelas(id_kelas)
        )
    """)
    
    # ========== TABEL NILAI ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai (
            id_nilai INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            semester TEXT,
            b_indo REAL,
            b_jawa REAL,
            b_inggris REAL,
            matematika REAL,
            ipas REAL,
            pjok REAL,
            pendidikan_pancasila REAL,
            btq REAL,
            pai REAL,
            seni_rupa REAL,
            seni_musik REAL,
            rata_nilai REAL,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)
    
    # ========== TABEL KEHADIRAN ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kehadiran (
            id_kehadiran INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            semester TEXT,
            hadir INTEGER DEFAULT 0,
            sakit INTEGER DEFAULT 0,
            izin INTEGER DEFAULT 0,
            alpha INTEGER DEFAULT 0,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)
    
    # ========== TABEL MOTIVASI ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motivasi (
            id_motivasi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            semester TEXT,
            skor_motivasi INTEGER,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)
    
    # ========== TABEL DISIPLIN ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disiplin_belajar (
            id_disiplin INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            semester TEXT,
            skor_disiplin INTEGER,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)
    
    # ========== TABEL HASIL PREDIKSI ==========
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hasil_prediksi (
            id_prediksi INTEGER PRIMARY KEY AUTOINCREMENT,
            id_siswa INTEGER,
            probabilitas REAL,
            hasil TEXT,
            tanggal_prediksi TEXT,
            FOREIGN KEY (id_siswa) REFERENCES siswa(id_siswa)
        )
    """)
    
    # ========== BUAT USER ADMIN DEFAULT ==========
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (nama, username, password, role)
            VALUES ('Admin', 'admin', 'admin123', 'admin')
        """)
        print("✅ User admin default: admin / admin123")
    
    # ========== BUAT USER GURU DEFAULT ==========
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='guru'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO users (nama, username, password, role)
            VALUES ('Guru', 'guru', 'guru123', 'guru')
        """)
        print("✅ User guru default: guru / guru123")
    
    conn.commit()
    conn.close()
    
    print("✅ Database SQLite berhasil diinisialisasi!")
    print(f"📁 Lokasi: {DB_PATH}")
    return True

if __name__ == "__main__":
    init_db()