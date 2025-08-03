# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy app files, assuming model.pkl and label_encoder.pkl are inside app/
COPY app/ /app
COPY app/model.pkl /app
COPY app/label_encoder.pkl /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
