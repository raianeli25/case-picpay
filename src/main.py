"""
Model API for loading, predicting with, and managing machine learning models.

This FastAPI application allows users to load machine learning models,
make predictions, and retrieve the history of inferences. The API provides
health check endpoints to ensure that the service is running properly.

Endpoints:
- GET /health: Checks the health status of the API.
- GET /: Welcomes users to the Model API.
- POST /model/load: Loads and persists a machine learning model from the specified path.
- GET /model/list: Lists all available models in the system.
- POST /model/predict: Makes predictions based on input data using the loaded model.
- GET /model/history: Retrieves the history of inferences made by the models.

"""

from fastapi import FastAPI
import uvicorn
from basemodels import InputData
from db_functions import save_pkl_model, load_pkl_model, \
predict_model, get_inferences_history, list_models

app = FastAPI()

@app.get("/health", status_code=200, tags=["health"], summary="Health check")
async def health():
    """Health check endpoint to verify that the API is running.

    Returns:
        JSON response with the status of the API.
    """
    return {"Status": "OK"}

@app.get("/", status_code=200, tags=["model_api"], summary="Health check")
async def welcome():
    """Welcome endpoint for the Model API.

    Returns:
        A welcome message for users accessing the API.
    """
    return "Wecolme to Model API"

@app.post("/model/load", tags=["model_api"], summary="Load model")
async def load_model(model_path: str):
    """Load and persist a machine learning model from a specified path.

    Args:
        model_path (str): The file path of the model to be loaded.

    Returns:
        JSON response indicating the success of the operation.
    """
    save_pkl_model(model_path)

    return {"message": "Model loaded and persisted successfully."}

@app.get("/model/list", tags=["model_api"], summary="List model")
async def get_models():
    """Retrieve a list of all available models.

    Returns:
        JSON response containing a list of models.
    """
    models = list_models()

    return {"models":list(models.find({},{}))}

@app.post("/model/predict", tags=["model_api"], summary="Make model predictions")
async def predict(data: InputData):
    """Make predictions using the loaded model and provided input data.

    Args:
        data (InputData): The input data for which predictions are to be made.

    Returns:
        The prediction result from the model.
    """
    model, model_id = load_pkl_model()

    result = predict_model(data,model,model_id)

    return result

@app.get("/model/history", tags=["model_api"], summary="List infereneces history")
async def get_history():
    """Retrieve the history of inferences made by the models.

    Returns:
        JSON response containing the status and list of inferences.
    """
    inferences = get_inferences_history()

    return {"status": "ok", "inferences": list(inferences.find({},{}))}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
