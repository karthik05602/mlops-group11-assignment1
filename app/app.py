from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)
model = joblib.load('app/model.pkl')
label_encoder = joblib.load('app/label_encoder.pkl')  # Load the encoder

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)
    predicted_label = label_encoder.inverse_transform([prediction[0]])[0]
    return jsonify({'prediction': predicted_label})

if __name__ == '__main__':
    app.run(debug=True)
