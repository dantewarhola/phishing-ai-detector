from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import joblib

# Load persisted artifacts
base_path = Path(__file__).resolve().parent.parent

# Build full paths to the model and vectorizer
model_path = base_path / "models" / "clf.joblib"
vect_path = base_path / "models" / "vect.joblib"

# Load model and vectorizer
model = joblib.load(model_path)
vect = joblib.load(vect_path)

app = FastAPI(
    title="Phish-AI Detector API",
    description="API to predict if an email is phishing or legitimate.",
    version="0.1.0"
)

class EmailRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    label: str
    score: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: EmailRequest):
    """Predict whether an email is phishing or legitimate."""
    # Vectorize and predict
    X = vect.transform([request.text])
    prob = float(model.predict_proba(X)[0, 1])
    label = "phishing" if prob > 0.5 else "legitimate"
    return PredictionResponse(label=label, score=prob)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
