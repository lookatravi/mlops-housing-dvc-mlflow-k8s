from flask import Flask, request, jsonify
import pandas as pd
from src.model_loader import load_model


app = Flask(__name__)
model = load_model()

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({"prediction": float(prediction)})

#  THIS WAS MISSING
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
