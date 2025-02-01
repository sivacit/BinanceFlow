from fastapi import FastAPI
import mlflow.pytorch
import torch
import numpy as np


app = FastAPI()

# Load model from MLflow
model_uri = "models:/PytorchModel/1"
model = mlflow.pytorch.load_model(model_uri)

@app.post("/predict")
def predict(data: list):
    input_tensor = torch.tensor(np.array(data), dtype=torch.float32)
    predictions = model(input_tensor).tolist()
    return {"predictions": predictions}

