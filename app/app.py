from flask import Flask, request, jsonify
import joblib
import pandas as pd
import logging
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Optional: custom metric for prediction endpoint
metrics.info('app_info', 'Iris prediction API', version='1.0.0')

# Load model and encoder
model = joblib.load('model.pkl')
label_encoder = joblib.load('label_encoder.pkl')

# Configure logging to a file
logging.basicConfig(
    filename='logs/iris_api.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

@app.route('/predict', methods=['POST'])
@metrics.counter('predict_requests_total', 'Total prediction requests')
def predict():
    data = request.get_json()
    input_df = pd.DataFrame([data])

    # Prediction
    prediction = model.predict(input_df)
    predicted_label = label_encoder.inverse_transform([prediction[0]])[0]

    # Log input and prediction
    logging.info(f"Input: {data} | Prediction: {predicted_label}")

    return jsonify({'prediction': predicted_label})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)