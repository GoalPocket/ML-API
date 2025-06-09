# 🧠 GoalPocket ML API

API ini digunakan untuk memprediksi saldo masa depan berdasarkan 7 minggu terakhir data keuangan user.

---

## 🚀 Endpoint

### `GET /`
Cek apakah API aktif.

### POST /predict
Melakukan prediksi saldo masa depan.

headers: application/json

✅ Request Body:
```json
{
  "data": [
    [asset, liability, income, expenses],
    [asset, liability, income, expenses],
    ...
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

### 📝 Teknologi
FastAPI

TensorFlow/Keras

Model: saldo_prediction_model.h5



