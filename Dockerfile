# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY app/ /app
COPY app/model.pkl /app
COPY app/label_encoder.pkl /app
COPY src/train.py /app/train.py
COPY data/iris-retrain.csv /data/iris-retrain.csv

# Create logs directory
RUN mkdir -p /app/logs

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
