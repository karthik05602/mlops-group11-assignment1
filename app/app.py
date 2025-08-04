import logging
import os
import subprocess

import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_pydantic import validate
from prometheus_flask_exporter import PrometheusMetrics
from pydantic import BaseModel

# -------------------------
# Define input schema
# -------------------------
class IrisFeatures(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

# -------------------------
# Initialize Flask app
# -------------------------
app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Iris prediction API', version='1.0.0')

# -------------------------
# Globals for model and encoder
# -------------------------
model = None
label_encoder = None

def load_model_and_encoder():
    global model, label_encoder
    model = joblib.load('model.pkl')
    label_encoder = joblib.load('label_encoder.pkl')

# Load initially
load_model_and_encoder()

# -------------------------
# Logging config
# -------------------------
logging.basicConfig(
    filename='logs/iris_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# -------------------------
# Prediction endpoint
# -------------------------
@app.route('/predict', methods=['POST'])
@validate()
@metrics.counter('predict_requests_total', 'Total prediction requests')
def predict(body: IrisFeatures):
    input_df = pd.DataFrame([body.dict()])
    prediction = model.predict(input_df)
    predicted_label = label_encoder.inverse_transform([prediction[0]])[0]
    logging.info(f"Input: {body.dict()} | Prediction: {predicted_label}")
    return jsonify({'prediction': predicted_label})

# -------------------------
# Retrain endpoint
# -------------------------
@app.route('/retrain', methods=['POST'])
def retrain_model():
    data = request.get_json()
    filename = data.get("filename")

    if not filename:
        return jsonify({"error": "Missing 'filename' in request body"}), 400

    file_path = os.path.join("/data", filename)
    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{filename}' not found in /data folder"}), 404

    try:
        result = subprocess.run(
            ["python", "train.py", "--input", file_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Reload model and encoder
        load_model_and_encoder()

        return jsonify({
            "message": f"Model retrained using {filename}"
        }), 200

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "Retraining failed",
            "details": e.stderr
        }), 500

# -------------------------
# Run the API
# -------------------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)