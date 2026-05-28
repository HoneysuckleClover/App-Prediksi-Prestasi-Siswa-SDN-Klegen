import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# =========================
# LOAD DATASET CSV
# =========================

try:
    df = pd.read_csv("dataset/dataset_siswa.csv")

    print("Dataset berhasil dibaca!")

except Exception as e:
    print("Gagal membaca dataset:", e)
    exit()

# =========================
# TAMPILKAN DATASET
# =========================

print("\n==============================")
print("DATASET")
print("==============================")

print(df.head())

# =========================
# CEK NULL
# =========================

print("\n==============================")
print("CEK DATA NULL")
print("==============================")

print(df.isnull().sum())

# Hapus data kosong
df = df.dropna()

# =========================
# CEK DUPLIKAT
# =========================

print("\n==============================")
print("CEK DUPLIKAT")
print("==============================")

print("Jumlah data duplikat:", df.duplicated().sum())

# =========================
# JUMLAH DATA
# =========================

print("\n==============================")
print("JUMLAH DATA")
print("==============================")

print("Total Data:", len(df))

# =========================
# DISTRIBUSI KELAS
# =========================

print("\n==============================")
print("DISTRIBUSI STATUS RISIKO")
print("==============================")

print(df["status_risiko"].value_counts())

# =========================
# FEATURE & TARGET
# =========================

X = df[
    [
        "rata_nilai",
        "hadir",
        "alpha",
        "skor_motivasi",
        "skor_disiplin"
    ]
]

y = df["status_risiko"]

# =========================
# SPLIT DATA
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =========================
# MODEL
# =========================

model = LogisticRegression(
    max_iter=1000
)

# =========================
# TRAINING MODEL
# =========================

model.fit(X_train, y_train)

print("\nModel berhasil dilatih!")

# =========================
# PREDIKSI
# =========================

y_pred = model.predict(X_test)

# =========================
# EVALUASI
# =========================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

# =========================
# HASIL EVALUASI
# =========================

print("\n==============================")
print("HASIL EVALUASI MODEL")
print("==============================")

print(f"Akurasi   : {accuracy:.2f}")
print(f"Precision : {precision:.2f}")
print(f"Recall    : {recall:.2f}")
print(f"F1-Score  : {f1:.2f}")

# =========================
# CONFUSION MATRIX
# =========================

print("\n==============================")
print("CONFUSION MATRIX")
print("==============================")

print(confusion_matrix(y_test, y_pred))

# =========================
# CLASSIFICATION REPORT
# =========================

print("\n==============================")
print("CLASSIFICATION REPORT")
print("==============================")

print(classification_report(
    y_test,
    y_pred,
    zero_division=0
))

# =========================
# SIMPAN MODEL
# =========================

joblib.dump(model, "model_logistic.pkl")

print("\nModel berhasil disimpan!")
print("Nama file : model_logistic.pkl")