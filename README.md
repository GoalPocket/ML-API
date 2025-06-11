# 🧠 ML-API REPO – GoalPocket ML Prediction
### 📡 Deskripsi
REST API berbasis FastAPI untuk memprediksi saldo keuangan pengguna berdasarkan histori 6 fitur: asset, liability, income, expenses, savings, loan.

Model ML dilatih dengan TensorFlow dan diekspor sebagai .h5 file, lalu digunakan untuk inferensi di endpoint /predict.

## 🗂 Struktur Utama

File/Folder	Deskripsi

main.py	Endpoint FastAPI untuk prediksi saldo

scaler_y.pkl	Scaler untuk inverse prediksi hasil model

saldo_prediction_model_2.h5	Model hasil pelatihan

requirements.txt	Daftar dependency Python

Dockerfile	Konfigurasi Docker container

### 🚀 Endpoint Prediksi
URL: /predict
Method: POST

Format Request 1: 6 fitur (digandakan 14x)
```json
{
  "data": [500000000, 400000000, 10000000, 20000000, 1000000, 5000000]
}
```
Format Request 2: 14 baris historis
```json
{
  "data": [
    [500000000, 400000000, 10000000, 20000000, 1000000, 5000000],
    ...
  ]
}
```

### 🔁 Response
```json
{
  "prediction": [
    "Rp120.000.000",
    "Rp125.000.000",
    ...
  ]
}
```
Jika scaler tidak tersedia:
```json
{
  "prediction": [[1.4415650367736816]],
  "note": "Hasil belum di-inverse karena scaler_y.pkl tidak ditemukan."
}

```

### 🐳 Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

### 📦 Requirements
fastapi

uvicorn

tensorflow

pydantic

python-multipart

numpy

joblib

scikit-learn

# ⚠️ Catatan
Model menggunakan custom loss function: MSE.

Jika scaler_y.pkl tidak tersedia, hasil prediksi tidak akan diubah ke format Rupiah.

Endpoint ini hanya memberikan estimasi saldo, bukan saran finansial resmi.
