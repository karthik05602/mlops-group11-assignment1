from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from flask_pydantic import validate
import joblib
import pandas as pd
import logging
from prometheus_flask_exporter import PrometheusMetrics

# Define input schema
class IrisFeatures(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Iris prediction API', version='1.0.0')

model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

logging.basicConfig(
    filename='logs/iris_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/predict', methods=['POST'])
@validate()
@metrics.counter('predict_requests_total', 'Total prediction requests')
def predict(body: IrisFeatures):
    input_df = pd.DataFrame([body.dict()])
    prediction = model.predict(input_df)
    predicted_label = label_encoder.inverse_transform([prediction[0]])[0]
    logging.info(f"Input: {body.dict()} | Prediction: {predicted_label}")
    return jsonify({'prediction': predicted_label})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
