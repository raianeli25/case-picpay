import pickle
import base64
from database import InMemoryDatabase
import pandas as pd
from fastapi import HTTPException

db = InMemoryDatabase()

def save_pkl_model(model_path):

    models = db.get_collection('models')

    try:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
            # Serialize the model and store it in MongoDB
            model_bytes = pickle.dumps(model)
            model_b64 = base64.b64encode(model_bytes).decode('utf-8')
            models.insert_one({"model": model_b64})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving model: {str(e)}")
  
    return model_b64

def load_pkl_model():

    try:
        # Retrieve the model from MongoDB
        models = db.get_collection('models')
        model_doc = models.find_one()

        # Deserialize the model
        model_bytes = base64.b64decode(model_doc["model"])

        model = pickle.loads(model_bytes)
        model_id = str(model_doc["_id"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")
    
    return model,model_id

def predict_model(data,model,model_id):

    try:
        df_data = pd.DataFrame([data.dict()])
        prediction_class = model.predict(df_data) 
        result = "atraso" if prediction_class == 1 else "sem atraso"
        inference_model = { 
        "model_id": model_id,    
        "prediction": result,
        "features": data
        }
        inference = db.get_collection('inferences')
        inference.insert_one(inference_model)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error on prediction: {str(e)}")


    return inference_model

def get_inferences_history():

    inferences = db.get_collection('inferences')

    return inferences

def list_models():

    models = db.get_collection('models')
    
    return models