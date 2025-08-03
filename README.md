# ML Ops Assignment - Deployment steps

This guide documents the complete steps to containerize, push, and deploy the changes in this repo using Podman/Docker and Docker Hub.

---

## 1. Build Docker Image Using Podman

```bash
cd mlops-group11-assignment1
podman build -t 2023ac05602/iris-api:latest .
```

---

## 2. Login to Docker Hub via Podman

```bash
podman login docker.io
Username: 2023ac05602
Token name: podman-mlops-token
```

---

## 3. Push Docker Image to Docker Hub

```bash
podman push docker.io/2023ac05602/iris-api:latest
```

---

## 4. Run the Container Locally

```bash
podman run -d -p 5000:5000 --name iris-api-container 2023ac05602/iris-api:latest
```

Test the API with:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"SepalLengthCm": 5.1, "SepalWidthCm": 3.5, "PetalLengthCm": 1.4, "PetalWidthCm": 0.2}'
```