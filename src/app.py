from flask import Flask, request, jsonify
import pandas as pd
from src.model_loader import load_model

app = Flask(__name__)

#  Load model ONCE at startup (important for Gunicorn)
model = load_model()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Enforce correct feature order (same as training)
    features = [
        "MedInc",
        "HouseAge",
        "AveRooms",
        "AveBedrms",
        "Population",
        "AveOccup",
        "Latitude",
        "Longitude",
    ]

    # Validate input
    for f in features:
        if f not in data:
            return jsonify({"error": f"Missing feature: {f}"}), 400

    # Create DataFrame exactly as model expects
    df = pd.DataFrame([[data[f] for f in features]], columns=features)

    # MLflow pyfunc prediction
    prediction = float(model.predict(df)[0])

    return jsonify({"prediction": prediction})

# Only for local dev (NOT used by Gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
