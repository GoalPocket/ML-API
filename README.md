# 🧠 GoalPocket ML API
REST API untuk aplikasi GoalPocket – platform perencanaan dan pelacakan keuangan. API ini juga terintegrasi dengan Machine Learning API untuk memprediksi saldo pengguna berdasarkan tren keuangan mereka.
---

## 🚀 Endpoint

### `GET /`
Cek apakah API aktif.

🚀 Endpoint Utama
✅ 1. Predict Saldo (ML Integration)
URL: POST /ml/predict-saldo

Deskripsi: Mengirim data historis keuangan user ke ML API dan mengembalikan prediksi saldo selanjutnya.

headers: application/json

📥 Request Body
```json
{
  "data": [
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    [asset, liability, income, expenses]
  ]
}

```
contoh:
```json
{
  "data": [
    [500000000, 400000000, 10000000, 20000000],
    [510000000, 390000000, 12000000, 21000000],
    [520000000, 380000000, 13000000, 22000000],
    [530000000, 370000000, 14000000, 23000000],
    [540000000, 360000000, 15000000, 24000000],
    [550000000, 350000000, 16000000, 25000000],
    [560000000, 340000000, 17000000, 26000000]
  ]
}
```

response:
```json
{
    "prediction": [
        [
            1.4415650367736816
        ]
    ]
}
```

### 📦 Teknologi
Node.js (Express)

PostgreSQL (via Prisma)

Axios (untuk koneksi ke ML API)

ML API (TensorFlow Model, deploy di Railway)

# 🌐 Public ML API yang digunakan:
https://ml-api-production-6fd5.up.railway.app/predict

Endpoint ini bersifat publik, tapi frontend harus mengakses melalui backend (/ml/predict-saldo) untuk keamanan dan fleksibilitas.

# 🧪 Testing
Kamu bisa menggunakan Postman untuk mencoba:

POST /ml/predict-saldo dengan body 7x4 seperti contoh

Melihat response prediction berupa array saldo prediksi
