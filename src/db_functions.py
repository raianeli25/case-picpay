"""
Module for saving, loading, predicting, and managing machine learning models
using an in-memory MongoDB database.

This module provides functions to serialize and deserialize machine learning
models with pickle, store them in a MongoDB collection, and perform predictions
on input data. It also allows retrieval of model and inference history.

Functions
---------
- save_pkl_model(model_path: str) -> str:
    Loads a model from a specified file path, serializes it, and stores it
    in the MongoDB collection.

- load_pkl_model() -> tuple:
    Retrieves the serialized model from the MongoDB collection, deserializes it,
    and returns the model along with its unique identifier.

- predict_model(data: Any, model: Any, model_id: str) -> dict:
    Takes input data, applies the model to make a prediction, and stores the
    inference details in the MongoDB collection.

- get_inferences_history() -> list:
    Retrieves all inference records from the MongoDB collection.

- list_models() -> list:
    Retrieves all stored models from the MongoDB collection.

Exceptions
----------
- Raises HTTPException with a 500 status code if there is an error during
  saving or loading models.
- Raises HTTPException with a 422 status code if there is an error during
  the prediction process.
"""
import pickle
import base64
from typing import Any, List, Tuple, Dict
import pandas as pd
from fastapi import HTTPException
from database import InMemoryDatabase
from basemodels import InputData

db = InMemoryDatabase()

def save_pkl_model(model_path: str) -> str:
    """Function save pkl model in memory using mongomock"""
    models = db.get_collection('models')

    try:
        with open(model_path, "rb") as file:
            model = pickle.load(file)
            # Serialize the model and store it in MongoDB
            model_bytes = pickle.dumps(model)
            model_b64 = base64.b64encode(model_bytes).decode('utf-8')
            models.insert_one({"model": model_b64})

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error saving model: {str(error)}")
    return model_b64

def load_pkl_model() -> Tuple[Any,str]:
    """Function load pkl model in memory using mongomock"""
    try:
        # Retrieve the model from MongoDB
        models = db.get_collection('models')
        model_doc = models.find_one()

        # Deserialize the model
        model_bytes = base64.b64decode(model_doc["model"])

        model = pickle.loads(model_bytes)
        model_id = str(model_doc["_id"])

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(error)}")

    return model,model_id

def predict_model(data:InputData,model:Any,model_id:str) -> Dict[str,Any]:
    """Function that make predictions with input data and model loaded"""
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
    except Exception as error:
        raise HTTPException(status_code=422, detail=f"Error on prediction: {str(error)}")

    return inference_model

def get_inferences_history() -> List[Dict[str, Any]]:
    """Function to list inferece history in memory with mongomock"""
    inferences = db.get_collection('inferences')

    return inferences

def list_models() -> List[Dict[str, Any]]:
    """Function to list model loaded in memory with mongomock"""
    models = db.get_collection('models')

    return models
