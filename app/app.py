from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import tensorflow as tf
from keras import layers, models

app = FastAPI()

model = models.load_model('../models/best_model.keras')

class PredictionInput(BaseModel):
    url: str

@app.post("/predict")
async def predict(input_data: PredictionInput):

    
    return {"phishing_probability": 1}