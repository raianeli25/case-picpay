from fastapi import FastAPI, HTTPException
from database import InMemoryDatabase
from basemodels import InputData
from aux_functions import save_pkl_model, load_pkl_model, predict_model, get_inferences_history
import pickle, base64
import pandas as pd
import uvicorn

app = FastAPI()
db = InMemoryDatabase()

@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    return {"Status": "OK"}

@app.post("/model/load")
async def load_model(model_path: str):

    save_pkl_model(model_path)
    
    return {"message": "Model loaded and persisted successfully."}

@app.get("/models/")
async def get_models():

    models = db.get_collection('models')

    return {"models":[x for x in models.find({},{})]}

@app.post("/model/predict")
async def predict(data: InputData):

    model, model_id = load_pkl_model()

    result = predict_model(data,model,model_id)

    return result

@app.get("/model/history", tags=["example"], summary="List all users")
async def get_history():

    inferences = get_inferences_history()
    
    return {"status": "ok", "inferences": [x for x in inferences.find({},{})]}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")