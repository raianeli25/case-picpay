"""
Unit tests for the FastAPI Model API.

This module contains tests for the endpoints of the Model API implemented in the
FastAPI application. The tests ensure that the API behaves as expected for various
scenarios, including successful requests and error handling.

Tests included:
- Welcome message
- Health check
- Listing models (including an empty case)
- Retrieving inference history (including an empty case)
- Loading models (both success and failure cases)
- Making predictions (both success and failure cases)
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_welcome():
    """Test the welcome endpoint."""
    response=client.get("/")
    assert response.status_code == 200
    assert response.json() == "Wecolme to Model API"

def test_health():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}

def test_get_models_empty():
    """Test retrieving models when none are available."""
    response = client.get("/model/list")
    assert response.status_code == 200
    assert response.json() == {"models": []}

def test_get_history_empty():
    """Test retrieving inference history when none are recorded."""
    response = client.get("/model/history")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "inferences": []}

def test_load_model_fail():
    """Test loading a model with an invalid path."""
    response = client.post("/model/load?model_path=src/artifacts/modelv2.pkl")
    assert response.status_code == 500

def test_load_model_successfull():
    """Test loading a model with a valid path."""
    response = client.post("/model/load?model_path=src/artifacts/model.pkl")
    assert response.status_code == 200
    assert response.json() == {"message": "Model loaded and persisted successfully."}

def test_predict_sucessfull():
    """Test making predictions with valid input data."""
    data = {
        "tailnum": "N37298",
        "carrier": "UA",
        "origin": "EWR",
        "dest": "RSW",
        "name": "United Air Lines Inc.",
        "distance": 1068
    }
    response = client.post("/model/predict", json=data)
    assert response.status_code == 200

def test_predict_fail():
    """Test making predictions with invalid input data."""
    data = []
    response = client.post("/model/predict", json=data)
    assert response.status_code == 422

def test_get_models():
    """Test retrieving the list of models."""
    response = client.get("/model/list")
    assert response.status_code == 200

def test_get_history():
    """Test retrieving the inference history."""
    response = client.get("/model/history")
    assert response.status_code == 200
