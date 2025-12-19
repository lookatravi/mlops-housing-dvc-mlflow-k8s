from flask import Flask, request, jsonify
import pandas as pd
from src.model_loader import load_model

app = Flask(__name__)

# load once at startup
model = load_model()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame([data])
    pred = model.predict(df)
    return jsonify({"prediction": float(pred[0])})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)