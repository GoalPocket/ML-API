from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware 
from tensorflow.keras.models import load_model  
from pydantic import BaseModel
from typing import List, Optional
import tensorflow as tf
import numpy as np
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger
logging.basicConfig(level=logging.INFO)

def my_custom_loss(y_true, y_pred):
    return tf.reduce_mean(tf.square(y_true - y_pred))

model = load_model('saldo_prediction_model.h5', custom_objects={'mse': my_custom_loss})
logging.info("✅ Model berhasil dimuat.")

# Format lama (list of lists)
class PredictionInput(BaseModel):
    data: List[List[float]]  # Bentuk: [[x1,x2,x3,x4], ..., (7x)]

# Format baru (satu input baris)
class SinglePredictionInput(BaseModel):
    asset: float
    liability: float
    income: float
    expenses: float

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/predict")
async def predict(request: Request):
    try:
        body = await request.json()

        # Jika body berisi key "data", gunakan format lama
        if "data" in body:
            input_data = PredictionInput(**body)
            logging.info(f"📥 Input format lama: {input_data.data}")
            data = np.array([input_data.data])  # (1, 7, 4)

        # Jika tidak ada key "data", coba format baru
        else:
            input_data = SinglePredictionInput(**body)
            logging.info(f"📥 Input format baru: {body}")
            data = np.array([[[
                input_data.asset,
                input_data.liability,
                input_data.income,
                input_data.expenses
            ]] * 7])  # Replikasi 7x agar jadi (1, 7, 4)

        logging.info(f"🔎 Bentuk input untuk model: {data.shape}")

        prediction = model.predict(data)
        result = prediction.tolist()
        return {"prediction": result}

    except Exception as e:
        logging.error(f"❌ Error saat prediksi: {e}")
        raise HTTPException(status_code=500, detail=str(e))
