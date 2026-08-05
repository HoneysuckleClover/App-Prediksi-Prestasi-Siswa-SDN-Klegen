import pandas as pd
import random

data = []

for i in range(1, 3001):

    # =========================
    # KEHADIRAN
    # =========================
    sakit = random.randint(0, 8)
    izin = random.randint(0, 8)
    alpha = random.randint(0, 15)

    total_hari = 100

    hadir = total_hari - sakit - izin - alpha

    if hadir < 60:
        hadir = 60

    # =========================
    # NILAI AKADEMIK
    # =========================
    nilai = random.randint(40, 100)

    # =========================
    # MOTIVASI
    # =========================
    motivasi = random.randint(40, 100)

    # =========================
    # DISIPLIN
    # =========================
    disiplin = random.randint(40, 100)

    # =========================
    # SKOR RISIKO
    # =========================
    skor_risiko = 0

    # NILAI
    if nilai < 70:
        skor_risiko += 2

    if nilai < 60:
        skor_risiko += 2

    # ALPHA
    if alpha > 5:
        skor_risiko += 2

    if alpha > 10:
        skor_risiko += 2

    # MOTIVASI
    if motivasi < 70:
        skor_risiko += 1

    if motivasi < 60:
        skor_risiko += 1

    # DISIPLIN
    if disiplin < 70:
        skor_risiko += 1

    if disiplin < 60:
        skor_risiko += 1

    # HADIR
    if hadir < 80:
        skor_risiko += 1

    if hadir < 70:
        skor_risiko += 1

    # =========================
    # LABEL RISIKO
    # =========================
    if skor_risiko >= 4:
        risiko = 1
    else:
        risiko = 0

    # =========================
    # TAMBAH VARIASI AGAR TIDAK
    # TERLALU KAKU
    # =========================
    if random.random() < 0.05:
        risiko = 1 - risiko

    data.append([
        i,
        f"Siswa {i}",
        nilai,
        hadir,
        sakit,
        izin,
        alpha,
        motivasi,
        disiplin,
        risiko
    ])

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(
    data,
    columns=[
        "id_siswa",
        "nama_siswa",
        "rata_nilai",
        "hadir",
        "sakit",
        "izin",
        "alpha",
        "skor_motivasi",
        "skor_disiplin",
        "status_risiko"
    ]
)

# =========================
# SIMPAN CSV
# =========================
df.to_csv(
    "dataset_siswa_3000.csv",
    index=False
)

print("Dataset berhasil dibuat!")
print(df.head())

print("\nDistribusi Label:")
print(df["status_risiko"].value_counts())