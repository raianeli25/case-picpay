from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_welcome():
    response=client.get("/")
    assert response.status_code == 200
    assert response.json() == "Wecolme to Model API"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"Status": "OK"}

def test_get_models_empty():
    response = client.get("/model/list")
    assert response.status_code == 200
    assert response.json() == {"models": []}

def test_get_history_empty():
    response = client.get("/model/history")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "inferences": []}

def test_load_model_fail():
    response = client.post("/model/load?model_path=src/artifacts/modelv2.pkl")
    assert response.status_code == 500

def test_load_model_successfull():
    response = client.post("/model/load?model_path=src/artifacts/model.pkl")
    assert response.status_code == 200
    assert response.json() == {"message": "Model loaded and persisted successfully."}

def test_predict_sucessfull():
    data = {
        "dep_delay": 24.0, 
        "carrier": "UA", 
        "origin": "EWR", 
        "dest": "RSW", 
        "air_time": 169.0, 
        "distance": 1068
    }
    response = client.post("/model/predict", json=data)
    assert response.status_code == 200

def test_predict_fail():
    data = []
    response = client.post("/model/predict", json=data)
    assert response.status_code == 422

def test_get_models():
    response = client.get("/model/list")
    assert response.status_code == 200

def test_get_history():
    response = client.get("/model/history")
    assert response.status_code == 200
