from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import joblib
import os

app = FastAPI()

# Cấu hình AWS S3
BUCKET_NAME = os.environ.get("CLOUD_BUCKET", "danghohai-mlops-bucket")
MODEL_KEY = "models/latest/model.pkl"
MODEL_PATH = os.path.expanduser("~/models/model.pkl")

def download_model():
    try:
        s3 = boto3.client('s3')
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print(f"Downloading model from s3://{BUCKET_NAME}/{MODEL_KEY}...")
        s3.download_file(BUCKET_NAME, MODEL_KEY, MODEL_PATH)
        print(f"Successfully downloaded model to {MODEL_PATH}")
    except Exception as e:
        print(f"Error downloading model: {e}")

# Tải model khi khởi động
download_model()

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

class PredictRequest(BaseModel):
    features: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    if len(req.features) != 12:
        raise HTTPException(status_code=400, detail="Expected 12 features")
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    prediction = model.predict([req.features])[0]
    labels = {0: "thấp", 1: "trung_bình", 2: "cao"}
    return {"prediction": int(prediction), "label": labels.get(int(prediction))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
