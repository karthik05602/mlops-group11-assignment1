# ML Ops Assignment - Deployment steps

This guide documents the complete steps to containerize, push, and deploy the changes in this repo using Podman/Docker and Docker Hub.

---

## 1. Build Docker Image Using Podman

```
cd mlops-group11-assignment1
podman build -t 2023ac05602/iris-api:latest .
```

---

## 2. Login to Docker Hub via Podman

```
podman login docker.io
Username: 2023ac05602
Token name: podman-mlops-token
```

---

## 3. Push Docker Image to Docker Hub

```
podman push docker.io/2023ac05602/iris-api:latest
```

---

## 4. Run the Container Locally

```
Run the script deploy_local.sh
./deploy.local.sh
```

Test the API with:

```
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"SepalLengthCm": 5.1, "SepalWidthCm": 3.5, "PetalLengthCm": 1.4, "PetalWidthCm": 0.2}'
```

## 5. Restart the container

```
Run the script deploy_local.sh
./restart.sh
```

Test the API with:

```
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"SepalLengthCm": 5.1, "SepalWidthCm": 3.5, "PetalLengthCm": 1.4, "PetalWidthCm": 0.2}'
```


## MLFlow UI

```
Run mlflow ui after running train.py file
```

### To activate venv in Mac
```
python3 -m venv venv
source venv/bin/activate
```

### Retraining the model

```
Use the below curl command to retrain the model for a file stored in the data folder.
Ensure that it has the exact schema as the original iris data.


curl --location 'http://localhost:5000/retrain' \
--header 'Content-Type: application/json' \
--data '{
    "filename": "iris-retrain.csv"
}'

```


## Steps for running and deploying the container in a Windows laptop

```
cd %USERPROFILE%\projects
git clone https://github.com/karthik05602/mlops-group11-assignment1.git
cd mlops-group11-assignment1

python -m venv .venv
.venv\Scripts\activate

pip install --upgrade pip

pip install fastapi uvicorn scikit-learn pandas joblib pydantic pytest mlflow flask-pydantic  prometheus-flask-exporter asgiref

pip freeze > requirements.txt

pytest -q

python src\train.py

python -m uvicorn app.app:asgi_app --host 0.0.0.0 --port 8000 –reload

curl -X POST http://127.0.0.1:8000/predict  -H "Content-Type: application/json"  -d "{ \"SepalLengthCm\":5.1, \"SepalWidthCm\":3.5, \"PetalLengthCm\":1.4, \"PetalWidthCm\":0.2 }"

mlflow ui
http://127.0.0.1:5000
```
