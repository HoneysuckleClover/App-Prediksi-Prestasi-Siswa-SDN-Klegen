# App Prediksi Prestasi Siswa SDN Klegen

Aplikasi berbasis Python untuk membantu **memprediksi prestasi siswa** (berdasarkan dataset & model yang dilatih) serta menyediakan modul manajemen data untuk peran pengguna.

## Fitur

- Login & Register
- Halaman peran:
  - Admin
  - Guru
  - Kepala Sekolah
- Modul prediksi prestasi siswa
- Modul pengelolaan data (siswa/kelas/user) sesuai kebutuhan sistem
- Komunikasi dengan database melalui `database/koneksi.py`

## Struktur Folder

- `main.py` : entry point aplikasi
- `database/` : koneksi & skema database
- `dataset/` : dataset siswa
- `ml/` : proses pelatihan model
- `models/` : file model (contoh: `model_logistic.pkl`)
- `pages/` : seluruh halaman UI per peran
- `assets/` : gambar/aset aplikasi
- `utils/`, `service/` : utilitas & service pendukung

## Prasyarat

- Python 3.x
- Git (opsional)
- Database (sesuaikan konfigurasi pada `database/koneksi.py`)

## Instalasi

1. Install dependency:

   ```bash
   pip install -r requirements.txt
   ```

2. (Opsional) Buat database menggunakan file:

   - `database/database_sdn_klegen.sql`

3. Sesuaikan konfigurasi database di `database/koneksi.py`.

## Menjalankan Aplikasi

```bash
python main.py
```

## Melatih Ulang Model (Jika Diperlukan)

Jika ingin melatih model ulang menggunakan dataset:

```bash
python ml/train_model.py
```

Hasil model biasanya akan disimpan di `models/`.

## Catatan

Pastikan file dan struktur folder sesuai repository ini, termasuk keberadaan model `models/model_logistic.pkl` (jika prediksi menggunakannya).

