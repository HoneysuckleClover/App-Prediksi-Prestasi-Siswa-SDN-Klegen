import pandas as pd
import sqlite3
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from database.koneksi_sqlite import connect_db
from tkinter import simpledialog

class ImportExportData:
    def __init__(self, parent):
        self.parent = parent
        self.df = None

    # ==========================================
    # DOWNLOAD TEMPLATE
    # ==========================================

    def download_template(self, template_type):
        """Download template Excel sesuai tipe"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=f"Simpan Template {template_type.capitalize()}"
        )

        if not file_path:
            return

        try:
            if template_type == "kelas":
                data = {
                    "Nama Kelas": ["VI-A", "VI-B"],
                    "Wali Kelas": ["Bu Ani", "Pak Budi"],
                    "Tahun Ajaran": ["2024/2025", "2024/2025"],
                    "Semester": ["Ganjil", "Genap"]
                }
                df = pd.DataFrame(data)

            elif template_type == "siswa":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Jenis Kelamin": ["L", "P"],
                    "Kelas": ["VI-A", "VI-A"],
                    "Tanggal Lahir": ["2012-05-10", "2012-08-15"],
                    "Alamat": ["Jl. Merdeka No.1", "Jl. Sudirman No.2"]
                }
                df = pd.DataFrame(data)

            elif template_type == "nilai":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "B.Indo": [85, 90],
                    "B.Jawa": [80, 85],
                    "B.Inggris": [75, 88],
                    "Matematika": [90, 85],
                    "IPAS": [88, 90],
                    "PJOK": [85, 82],
                    "Pancasila": [82, 88],
                    "BTQ": [90, 85],
                    "PAI": [85, 90],
                    "Seni Rupa": [80, 88],
                    "Seni Musik": [85, 90]
                }
                df = pd.DataFrame(data)

            elif template_type == "kehadiran":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "Hadir": [25, 28],
                    "Sakit": [2, 0],
                    "Izin": [1, 0],
                    "Alpha": [0, 0]
                }
                df = pd.DataFrame(data)

            elif template_type == "motivasi":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "Skor Motivasi": [85, 90]
                }
                df = pd.DataFrame(data)

            elif template_type == "disiplin":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "Skor Disiplin": [82, 88]
                }
                df = pd.DataFrame(data)

            elif template_type == "all_admin":
                data = {
                    "Nama Kelas": ["VI-A", "VI-B"],
                    "Tahun Ajaran": ["2024/2025", "2024/2025"],
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Jenis Kelamin": ["L", "P"],
                    "Tanggal Lahir": ["2012-05-10", "2012-08-15"],
                    "Alamat": ["Jl. Merdeka No.1", "Jl. Sudirman No.2"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "B.Indo": [85, 90],
                    "B.Jawa": [80, 85],
                    "B.Inggris": [75, 88],
                    "Matematika": [90, 85],
                    "IPAS": [88, 90],
                    "PJOK": [85, 82],
                    "Pancasila": [82, 88],
                    "BTQ": [90, 85],
                    "PAI": [85, 90],
                    "Seni Rupa": [80, 88],
                    "Seni Musik": [85, 90],
                    "Hadir": [25, 28],
                    "Sakit": [2, 0],
                    "Izin": [1, 0],
                    "Alpha": [0, 0],
                    "Skor Motivasi": [85, 90],
                    "Skor Disiplin": [82, 88]
                }
                df = pd.DataFrame(data)

            elif template_type == "all_guru":
                data = {
                    "NIS": ["001", "002"],
                    "Nama Siswa": ["Ahmad Fauzi", "Siti Rahayu"],
                    "Semester": ["Ganjil", "Ganjil"],
                    "B.Indo": [85, 90],
                    "B.Jawa": [80, 85],
                    "B.Inggris": [75, 88],
                    "Matematika": [90, 85],
                    "IPAS": [88, 90],
                    "PJOK": [85, 82],
                    "Pancasila": [82, 88],
                    "BTQ": [90, 85],
                    "PAI": [85, 90],
                    "Seni Rupa": [80, 88],
                    "Seni Musik": [85, 90],
                    "Hadir": [25, 28],
                    "Sakit": [2, 0],
                    "Izin": [1, 0],
                    "Alpha": [0, 0],
                    "Skor Motivasi": [85, 90],
                    "Skor Disiplin": [82, 88]
                }
                df = pd.DataFrame(data)

            df.to_excel(file_path, index=False)
            messagebox.showinfo("Sukses", f"Template {template_type} berhasil dibuat!\nLokasi: {file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"Gagal membuat template:\n{str(e)}")

    # ==========================================
    # IMPORT DATA
    # ==========================================

    def import_data(self, template_type):
        """Import data dari Excel"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")],
            title=f"Pilih file {template_type.capitalize()}"
        )

        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path)

            if df.empty:
                messagebox.showwarning("Peringatan", "File kosong!")
                return

            preview_text = df.head(5).to_string()

            if not messagebox.askyesno("Konfirmasi",
                f"Akan mengimport {len(df)} data.\n\nPreview:\n{preview_text}\n\nLanjutkan?"):
                return

            conn = connect_db()
            cursor = conn.cursor()

            success = 0
            failed = 0
            errors = []

            for index, row in df.iterrows():
                try:
                    if template_type == "kelas":
                        self._import_kelas(cursor, row)
                    elif template_type == "siswa":
                        self._import_siswa(cursor, row)
                    elif template_type == "nilai":
                        self._import_nilai(cursor, row)
                    elif template_type == "kehadiran":
                        self._import_kehadiran(cursor, row)
                    elif template_type == "motivasi":
                        self._import_motivasi(cursor, row)
                    elif template_type == "disiplin":
                        self._import_disiplin(cursor, row)
                    elif template_type == "all_admin":
                        self._import_all_admin(cursor, row)
                    elif template_type == "all_guru":
                        self._import_all_guru(cursor, row)
                    success += 1
                except Exception as e:
                    failed += 1
                    errors.append(f"Baris {index+2}: {str(e)}")

            conn.commit()
            conn.close()

            msg = f"✅ Import selesai!\n\n✅ Berhasil: {success}\n❌ Gagal: {failed}"
            if errors:
                msg += f"\n\nDetail error:\n" + "\n".join(errors[:5])
                if len(errors) > 5:
                    msg += f"\n... dan {len(errors)-5} error lainnya"

            messagebox.showinfo("Hasil Import", msg)

            if hasattr(self.parent, 'load_data'):
                self.parent.load_data()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal import data:\n{str(e)}")

    # ==========================================
    # IMPORT FUNGSI PER TABEL
    # ==========================================
    
    def get_guru_list(self):
        """Ambil daftar guru dari database"""
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id_user, nama FROM users WHERE role='guru' ORDER BY nama")
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            print(f"Error ambil daftar guru: {e}")
            return []

    def _import_kelas(self, cursor, row):   
        # Cari user (guru) berdasarkan nama
        guru = str(row['Wali Kelas']).strip() if pd.notna(row['Wali Kelas']) else None
        id_user = None
        
        if guru:
            # CARI USER DENGAN ROLE GURU (case insensitive)
            cursor.execute("""
                SELECT id_user FROM users 
                WHERE LOWER(nama)=LOWER(?) AND role='guru'
            """, (guru,))
            user = cursor.fetchone()
            
            if user:
                id_user = user[0]
                print(f"✅ Guru '{guru}' ditemukan! ID: {id_user}")
            else:
                # Coba LIKE
                cursor.execute("""
                    SELECT id_user, nama FROM users 
                    WHERE nama LIKE ? AND role='guru'
                """, (f"%{guru}%",))
                user = cursor.fetchone()
                
                if user:
                    id_user = user[0]
                    print(f"⚠️ Guru '{guru}' ditemukan dengan LIKE! ID: {id_user}")
                else:
                    # Guru tidak ditemukan, tampilkan daftar guru untuk dipilih
                    print(f"❌ Guru '{guru}' TIDAK DITEMUKAN di database!")
                    
                    # Ambil daftar guru
                    guru_list = self.get_guru_list()
                    if guru_list:
                        # Buat daftar nama guru
                        guru_names = [f"{row[1]} (ID: {row[0]})" for row in guru_list]
                        guru_names.append("SKIP (kosongkan wali kelas)")
                        
                        # Tampilkan dialog pilihan
                        from tkinter import Toplevel, Listbox, Button, Scrollbar, Label
                        import tkinter as tk
                        
                        # Buat window popup
                        popup = tk.Toplevel()
                        popup.title("Pilih Wali Kelas")
                        popup.geometry("400x300")
                        popup.configure(bg="#1E293B")
                        
                        Label(popup, text=f"Guru '{guru}' tidak ditemukan!\nPilih wali kelas untuk kelas ini:", 
                            bg="#1E293B", fg="white", font=("Segoe UI", 11)).pack(pady=10)
                        
                        # Listbox
                        listbox = Listbox(popup, bg="#334155", fg="white", 
                                        selectbackground="#2563EB", height=10, font=("Segoe UI", 10))
                        listbox.pack(padx=20, pady=5, fill="both", expand=True)
                        
                        for item in guru_names:
                            listbox.insert("end", item)
                        
                        # Variabel untuk menyimpan pilihan
                        selected = [None]
                        
                        def on_select():
                            selection = listbox.curselection()
                            if selection:
                                selected[0] = listbox.get(selection[0])
                                popup.destroy()
                        
                        def on_skip():
                            selected[0] = "SKIP"
                            popup.destroy()
                        
                        # Tombol
                        btn_frame = tk.Frame(popup, bg="#1E293B")
                        btn_frame.pack(pady=10)
                        
                        Button(btn_frame, text="Pilih", command=on_select,
                            bg="#2563EB", fg="white", padx=20, pady=5, font=("Segoe UI", 10)).pack(side="left", padx=5)
                        Button(btn_frame, text="Lewati", command=on_skip,
                            bg="#475569", fg="white", padx=20, pady=5, font=("Segoe UI", 10)).pack(side="left", padx=5)
                        
                        # Tunggu popup selesai
                        popup.grab_set()
                        popup.wait_window()
                        
                        # Proses hasil pilihan
                        if selected[0] and selected[0] != "SKIP":
                            # Ambil ID dari pilihan "Nama (ID: X)"
                            try:
                                id_str = selected[0].split("ID: ")[1].replace(")", "")
                                id_user = int(id_str)
                                print(f"✅ User memilih guru ID: {id_user}")
                            except:
                                pass
                        elif selected[0] == "SKIP":
                            id_user = None
                            print(f"ℹ️ User memilih untuk skip wali kelas")
        
        # Insert kelas dengan id_user (bisa NULL jika guru tidak ditemukan)
        cursor.execute("""
            INSERT OR IGNORE INTO kelas (nama_kelas, id_user, tahun_ajaran, semester)
            VALUES (?, ?, ?, ?)
        """, (
            str(row['Nama Kelas']).strip(),
            id_user,
            str(row['Tahun Ajaran']).strip() if pd.notna(row['Tahun Ajaran']) else "2024/2025",
            str(row['Semester']).strip() if pd.notna(row['Semester']) else "Ganjil"
        ))

    def _import_siswa(self, cursor, row):
        cursor.execute("SELECT id_kelas FROM kelas WHERE nama_kelas=?", (str(row['Kelas']).strip(),))
        kelas = cursor.fetchone()

        if not kelas:
            cursor.execute("INSERT INTO kelas (nama_kelas, semester) VALUES (?, ?)", 
                          (str(row['Kelas']).strip(), "Ganjil"))
            kelas_id = cursor.lastrowid
        else:
            kelas_id = kelas[0]

        cursor.execute("""
            INSERT OR IGNORE INTO siswa 
            (nis, nama_siswa, jenis_kelamin, id_kelas, tanggal_lahir, alamat)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(row['NIS']).strip(),
            str(row['Nama Siswa']).strip(),
            str(row['Jenis Kelamin']).strip(),
            kelas_id,
            str(row['Tanggal Lahir']).strip() if pd.notna(row['Tanggal Lahir']) else None,
            str(row['Alamat']).strip() if pd.notna(row['Alamat']) else None
        ))

    def _import_nilai(self, cursor, row):
        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()
        if not siswa:
            raise Exception(f"Siswa dengan NIS {row['NIS']} tidak ditemukan!")

        nilai_list = [
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0
        ]
        rata = round(sum(nilai_list) / 11, 2)

        cursor.execute("""
            INSERT INTO nilai 
            (id_siswa, semester, b_indo, b_jawa, b_inggris, matematika, 
             ipas, pjok, pendidikan_pancasila, btq, pai, seni_rupa, seni_musik, rata_nilai)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            siswa[0], str(row['Semester']).strip(),
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0,
            rata
        ))

    def _import_kehadiran(self, cursor, row):
        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()
        if not siswa:
            raise Exception(f"Siswa dengan NIS {row['NIS']} tidak ditemukan!")

        cursor.execute("""
            INSERT INTO kehadiran (id_siswa, semester, hadir, sakit, izin, alpha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            siswa[0], str(row['Semester']).strip(),
            int(row['Hadir']) if pd.notna(row['Hadir']) else 0,
            int(row['Sakit']) if pd.notna(row['Sakit']) else 0,
            int(row['Izin']) if pd.notna(row['Izin']) else 0,
            int(row['Alpha']) if pd.notna(row['Alpha']) else 0
        ))

    def _import_motivasi(self, cursor, row):
        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()
        if not siswa:
            raise Exception(f"Siswa dengan NIS {row['NIS']} tidak ditemukan!")

        cursor.execute("""
            INSERT INTO motivasi (id_siswa, semester, skor_motivasi)
            VALUES (?, ?, ?)
        """, (
            siswa[0], str(row['Semester']).strip(),
            int(row['Skor Motivasi']) if pd.notna(row['Skor Motivasi']) else 0
        ))

    def _import_disiplin(self, cursor, row):
        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()
        if not siswa:
            raise Exception(f"Siswa dengan NIS {row['NIS']} tidak ditemukan!")

        cursor.execute("""
            INSERT INTO disiplin_belajar (id_siswa, semester, skor_disiplin)
            VALUES (?, ?, ?)
        """, (
            siswa[0], str(row['Semester']).strip(),
            int(row['Skor Disiplin']) if pd.notna(row['Skor Disiplin']) else 0
        ))

    def _import_all_admin(self, cursor, row):
        """Import semua data sekaligus (Admin)"""
        # 1. Kelas 
        guru = str(row['Wali Kelas']).strip() if pd.notna(row['Wali Kelas']) else None
        id_user = None
        
        if guru:
            cursor.execute("""
                SELECT id_user FROM users 
                WHERE LOWER(nama)=LOWER(?) AND role='guru'
            """, (guru,))
            user = cursor.fetchone()
            
            if user:
                id_user = user[0]
            else:
                cursor.execute("""
                    SELECT id_user, nama FROM users 
                    WHERE nama LIKE ? AND role='guru'
                """, (f"%{guru}%",))
                user = cursor.fetchone()
                
                if user:
                    id_user = user[0]
                else:
                    # Tampilkan popup pilih guru
                    guru_list = self.get_guru_list()
                    if guru_list:
                        guru_names = [f"{row[1]} (ID: {row[0]})" for row in guru_list]
                        guru_names.append("SKIP")
                        
                        from tkinter import Toplevel, Listbox, Button, Label
                        import tkinter as tk
                        
                        popup = tk.Toplevel()
                        popup.title("Pilih Wali Kelas")
                        popup.geometry("400x300")
                        popup.configure(bg="#1E293B")
                        
                        Label(popup, text=f"Guru '{guru}' tidak ditemukan!\nPilih wali kelas:", 
                            bg="#1E293B", fg="white", font=("Segoe UI", 11)).pack(pady=10)
                        
                        listbox = Listbox(popup, bg="#334155", fg="white", 
                                        selectbackground="#2563EB", height=10, font=("Segoe UI", 10))
                        listbox.pack(padx=20, pady=5, fill="both", expand=True)
                        
                        for item in guru_names:
                            listbox.insert("end", item)
                        
                        selected = [None]
                        
                        def on_select():
                            selection = listbox.curselection()
                            if selection:
                                selected[0] = listbox.get(selection[0])
                                popup.destroy()
                        
                        def on_skip():
                            selected[0] = "SKIP"
                            popup.destroy()
                        
                        btn_frame = tk.Frame(popup, bg="#1E293B")
                        btn_frame.pack(pady=10)
                        
                        Button(btn_frame, text="Pilih", command=on_select,
                            bg="#2563EB", fg="white", padx=20, pady=5).pack(side="left", padx=5)
                        Button(btn_frame, text="Lewati", command=on_skip,
                            bg="#475569", fg="white", padx=20, pady=5).pack(side="left", padx=5)
                        
                        popup.grab_set()
                        popup.wait_window()
                        
                        if selected[0] and selected[0] != "SKIP":
                            try:
                                id_str = selected[0].split("ID: ")[1].replace(")", "")
                                id_user = int(id_str)
                            except:
                                pass

        cursor.execute("""
            INSERT OR IGNORE INTO kelas (nama_kelas, id_user, tahun_ajaran, semester)
            VALUES (?, ?, ?, ?)
        """, (
            str(row['Nama Kelas']).strip(),
            id_user,
            str(row['Tahun Ajaran']).strip() if pd.notna(row['Tahun Ajaran']) else "2024/2025",
            str(row['Semester']).strip() if pd.notna(row['Semester']) else "Ganjil"
        ))

        # 2. Siswa
        cursor.execute("SELECT id_kelas FROM kelas WHERE nama_kelas=?", (str(row['Nama Kelas']).strip(),))
        kelas = cursor.fetchone()
        if not kelas:
            raise Exception(f"Kelas {row['Nama Kelas']} tidak ditemukan!")

        kelas_id = kelas[0]

        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()

        if not siswa:
            cursor.execute("""
                INSERT INTO siswa (nis, nama_siswa, jenis_kelamin, id_kelas, tanggal_lahir, alamat)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                str(row['NIS']).strip(),
                str(row['Nama Siswa']).strip(),
                str(row['Jenis Kelamin']).strip(),
                kelas_id,
                str(row['Tanggal Lahir']).strip() if pd.notna(row['Tanggal Lahir']) else None,
                str(row['Alamat']).strip() if pd.notna(row['Alamat']) else None
            ))
            cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
            siswa = cursor.fetchone()

        siswa_id = siswa[0]

        # 3. Nilai
        nilai_list = [
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0
        ]
        rata = round(sum(nilai_list) / 11, 2)

        cursor.execute("""
            INSERT INTO nilai 
            (id_siswa, semester, b_indo, b_jawa, b_inggris, matematika, 
             ipas, pjok, pendidikan_pancasila, btq, pai, seni_rupa, seni_musik, rata_nilai)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0,
            rata
        ))

        # 4. Kehadiran
        cursor.execute("""
            INSERT INTO kehadiran (id_siswa, semester, hadir, sakit, izin, alpha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Hadir']) if pd.notna(row['Hadir']) else 0,
            int(row['Sakit']) if pd.notna(row['Sakit']) else 0,
            int(row['Izin']) if pd.notna(row['Izin']) else 0,
            int(row['Alpha']) if pd.notna(row['Alpha']) else 0
        ))

        # 5. Motivasi
        cursor.execute("""
            INSERT INTO motivasi (id_siswa, semester, skor_motivasi)
            VALUES (?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Skor Motivasi']) if pd.notna(row['Skor Motivasi']) else 0
        ))

        # 6. Disiplin
        cursor.execute("""
            INSERT INTO disiplin_belajar (id_siswa, semester, skor_disiplin)
            VALUES (?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Skor Disiplin']) if pd.notna(row['Skor Disiplin']) else 0
        ))

    def _import_all_guru(self, cursor, row):
        """Import semua data sekaligus (Guru)"""
        # 1. Cari siswa berdasarkan NIS
        cursor.execute("SELECT id_siswa FROM siswa WHERE nis=?", (str(row['NIS']).strip(),))
        siswa = cursor.fetchone()
        if not siswa:
            raise Exception(f"Siswa dengan NIS {row['NIS']} tidak ditemukan! Import gagal.")

        siswa_id = siswa[0]

        # 2. Nilai
        nilai_list = [
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0
        ]
        rata = round(sum(nilai_list) / 11, 2)

        cursor.execute("""
            INSERT INTO nilai 
            (id_siswa, semester, b_indo, b_jawa, b_inggris, matematika, 
             ipas, pjok, pendidikan_pancasila, btq, pai, seni_rupa, seni_musik, rata_nilai)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            float(row['B.Indo']) if pd.notna(row['B.Indo']) else 0,
            float(row['B.Jawa']) if pd.notna(row['B.Jawa']) else 0,
            float(row['B.Inggris']) if pd.notna(row['B.Inggris']) else 0,
            float(row['Matematika']) if pd.notna(row['Matematika']) else 0,
            float(row['IPAS']) if pd.notna(row['IPAS']) else 0,
            float(row['PJOK']) if pd.notna(row['PJOK']) else 0,
            float(row['Pancasila']) if pd.notna(row['Pancasila']) else 0,
            float(row['BTQ']) if pd.notna(row['BTQ']) else 0,
            float(row['PAI']) if pd.notna(row['PAI']) else 0,
            float(row['Seni Rupa']) if pd.notna(row['Seni Rupa']) else 0,
            float(row['Seni Musik']) if pd.notna(row['Seni Musik']) else 0,
            rata
        ))

        # 3. Kehadiran
        cursor.execute("""
            INSERT INTO kehadiran (id_siswa, semester, hadir, sakit, izin, alpha)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Hadir']) if pd.notna(row['Hadir']) else 0,
            int(row['Sakit']) if pd.notna(row['Sakit']) else 0,
            int(row['Izin']) if pd.notna(row['Izin']) else 0,
            int(row['Alpha']) if pd.notna(row['Alpha']) else 0
        ))

        # 4. Motivasi
        cursor.execute("""
            INSERT INTO motivasi (id_siswa, semester, skor_motivasi)
            VALUES (?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Skor Motivasi']) if pd.notna(row['Skor Motivasi']) else 0
        ))

        # 5. Disiplin
        cursor.execute("""
            INSERT INTO disiplin_belajar (id_siswa, semester, skor_disiplin)
            VALUES (?, ?, ?)
        """, (
            siswa_id, str(row['Semester']).strip(),
            int(row['Skor Disiplin']) if pd.notna(row['Skor Disiplin']) else 0
        ))