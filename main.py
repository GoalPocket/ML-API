from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from pydantic import BaseModel
from typing import List
import tensorflow as tf
import numpy as np
import logging
import joblib
import os

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger
logging.basicConfig(level=logging.INFO)

# Fungsi custom loss (harus cocok dengan model training)
def my_custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

# Path absolut ke folder saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model
model_path = os.path.join(BASE_DIR, "saldo_prediction_model_2.h5")
model = load_model(model_path, custom_objects={"mse": my_custom_loss})
logging.info("✅ Model berhasil dimuat.")

# Load scaler
scaler_y_path = os.path.join(BASE_DIR, "scaler_y.pkl")
try:
    scaler_y = joblib.load(scaler_y_path)
    logging.info("✅ Scaler untuk target berhasil dimuat.")
except Exception as e:
    scaler_y = None
    logging.warning(f"⚠️ Gagal memuat scaler_y.pkl: {e}")

# Format input dari klien
class SingleInput(BaseModel):
    data: List[float]  # Contoh: [asset, liability, income, expenses, savings, loan]

class MultipleInput(BaseModel):
    data: List[List[float]]  # Contoh: [[...6 fitur...], [...], ...] sebanyak 14x

# Fungsi untuk format ke Rupiah
def format_rupiah(amount):
    try:
        return f"Rp{int(round(amount)):,}".replace(",", ".")
    except:
        return "Rp0"

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/predict")
async def predict(request: Request):
    try:
        body = await request.json()

        # Format 2: data berisi 14 baris
        if isinstance(body["data"][0], list):
            input_data = MultipleInput(**body)
            if len(input_data.data) != 14 or any(len(row) != 6 for row in input_data.data):
                raise HTTPException(status_code=400, detail="Format data harus 14 baris, masing-masing 6 fitur.")
            data = np.array([input_data.data], dtype=np.float32)  # (1, 14, 6)

        # Format 1: data berisi 6 fitur, digandakan 14x
        else:
            input_data = SingleInput(**body)
            if len(input_data.data) != 6:
                raise HTTPException(status_code=400, detail="Input harus berisi tepat 6 fitur.")
            data = np.array([[input_data.data] * 14], dtype=np.float32)  # (1, 14, 6)

        # 🚨 Validasi jika seluruh input bernilai 0
        if np.all(data == 0):
            raise HTTPException(status_code=400, detail="Input tidak boleh seluruhnya bernilai 0.")

        logging.info(f"🔎 Shape input ke model: {data.shape}")
        prediction = model.predict(data)

        # Inverse transform jika scaler tersedia
        if scaler_y:
            prediction_rescaled = scaler_y.inverse_transform(prediction)
            formatted = [format_rupiah(val) for val in prediction_rescaled[0]]
            return {"prediction": formatted}
        else:
            return {
                "prediction": prediction.tolist(),
                "note": "Hasil belum di-inverse karena scaler_y.pkl tidak ditemukan."
            }

    except HTTPException as http_exc:
        # Penting! Jangan ubah status code error validasi
        raise http_exc
    except Exception as e:
        logging.error(f"❌ Error saat prediksi: {e}")
        raise HTTPException(status_code=500, detail="Terjadi kesalahan internal pada server.")
