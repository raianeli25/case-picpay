from fastapi import FastAPI
from database import InMemoryDatabase
import pickle
import pandas as pd
from pydantic import BaseModel
from bson import ObjectId
import uvicorn
import base64


app = FastAPI()


@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    return {"status": "ok"}

# Define a model to hold the model metadata
class ModelMetadata(BaseModel):
    id: str
    name: str  # You can include model name or any identifier
    parameters: dict  # Store model parameters or relevant information

@app.post("/model/load")
async def load_model(model_path: str):
    
    db = InMemoryDatabase()
    models = db.get_collection('models')

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
            # Serialize the model and store it in MongoDB
            model_bytes = pickle.dumps(model)
            model_b64 = base64.b64encode(model_bytes).decode('utf-8')
            models.insert_one({"model": model_b64})
            return {"message": "Model loaded and persisted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/")
async def get_models():
    db = InMemoryDatabase()
    models = db.get_collection('models')

    return {"models":[x for x in models.find({},{})]}

@app.post("/model/predict")
async def predict(data: dict):
    db = InMemoryDatabase()
    print(data)
    df_data = pd.DataFrame([data])
    print(df_data.head())
    
    
        # Retrieve the model from MongoDB
    models = db.get_collection('models')

    model_doc = models.find_one()
    print(model_doc)
    if model_doc is None:
        raise HTTPException(status_code=500, detail="No model loaded in database.")
    
    # Deserialize the model
    model_bytes = base64.b64decode(model_doc["model"])
    model = pickle.loads(model_bytes)

    prediction_class = model.predict(df_data) 
    result = "Atrasará" if prediction_class == 1 else "Não atrasará"
    inference_model = { 
    "prediction": result,
    "features": data
    }
    inference = db.get_collection('inferences')
    inference.insert_one(inference_model)
    return inference_model

@app.get("/model/history", tags=["example"], summary="List all users")
async def history():
    db = InMemoryDatabase()
    inferences = db.get_collection('inferences')
    history_inferences = [x for x in inferences.find({},{})]
    print(history_inferences)
    return {"status": "ok", "inferences": [x for x in inferences.find({},{})]}

@app.post("/user/", tags=["example"], summary="Insert user")
async def insert(data: dict):
    db = InMemoryDatabase()
    users = db.get_collection('users')
    users.insert_one(data)
    return {"status": "ok"}

@app.get("/user/{name}", status_code=200, tags=["example"], summary="Get user by name")
async def get(name: str):
    db = InMemoryDatabase()
    users = db.get_collection('users')
    user = users.find_one({"name": name})
    return {"status": "ok", "user": user}

@app.get("/user/", tags=["example"], summary="List all users")
async def list():
    db = InMemoryDatabase()
    users = db.get_collection('users')
    return {"status": "ok", "users": [x for x in users.find({},{"_id": 0})]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")