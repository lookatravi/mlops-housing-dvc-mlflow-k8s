# MLOps California Housing Prediction  
**DVC + AWS S3 + MLflow**

This project demonstrates a **simple, real-world MLOps workflow** using:
- DVC for dataset versioning
- AWS S3 for dataset storage
- MLflow for experiment tracking
- Python + Scikit-learn for model training

The goal is to show **how data, code, and experiments are managed separately** in a production-style ML system.

---

## 📌 Problem Statement

We want to **predict house prices** using machine learning.

In real projects:
- Datasets are large
- Code changes frequently
- Models must be reproducible

This project solves these problems using **MLOps best practices**.

---

## 🛠 Tech Stack (What & Why)

### Git
- **What:** Version control for source code  
- **Why:** Code is small and changes often

### DVC (Data Version Control)
- **What:** Version control for datasets  
- **Why:** Git is not suitable for large data files

### AWS S3
- **What:** Cloud storage for datasets  
- **Why:** Scalable, durable, and cheap for large data

### MLflow
- **What:** Experiment tracking tool  
- **Why:** Track metrics, parameters, and models

### Python + Scikit-learn
- **What:** Model development and training  
- **Why:** Simple, reliable, and widely used

---

## 📁 Project Structure

.
├── data/
│   ├── housing.csv.dvc     # Dataset pointer tracked by Git
│   └── housing.csv         # Real dataset (pulled from S3)
│
├── src/
│   ├── make_dataset.py     # Creates the dataset
│   └── train.py            # Trains the ML model
│
├── mlruns/                 # Local MLflow experiment logs
├── requirements.txt
├── README.md
└── .dvc/

---

## ⚙️ Prerequisites

brew install git awscli dvc python

aws configure
aws sts get-caller-identity

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

---

## 🚀 Run Steps (Quick)

git clone https://github.com/lookatravi/mlops-housing-dvc-mlflow-k8s.git
cd mlops-housing-dvc-mlflow-k8s

dvc pull

MLFLOW_TRACKING_URI="file:./mlruns" python3 src/train.py --run run-1

mlflow ui --backend-store-uri file:./mlruns --host 127.0.0.1 --port 7006

---

---

## 🌐 Model Serving – Exposing the Model as an API (Flask + WSGI)

Training a model is not enough in real systems.  
The model must be **served as an API** so other applications can use it.

In this project, we expose the trained housing model as a **REST API** using Flask.

---

## 🧠 What is happening here (Simple)

- Model is trained and stored using **MLflow**
- API loads the trained model from a **specific MLflow run**
- Client sends house features as JSON
- API returns predicted house price

---

## 📂 API Files Added

```text
src/
├── app.py           # Flask API endpoints
├── model_loader.py  # Loads model from MLflow
└── wsgi.py          # WSGI entry 

---

## 🚀 Running the API with Gunicorn (WSGI – Production Ready)

Flask’s built-in server is **only for development**.  
In real systems, we use **Gunicorn**, a production-grade **WSGI server**.

Gunicorn:
- Manages multiple worker processes
- Handles concurrent requests
- Is widely used in production (AWS, Docker, Kubernetes)

---

## 🧠 What is WSGI and Why Gunicorn?

### What is WSGI?
WSGI (Web Server Gateway Interface) is a standard for running Python web apps.

### Why Gunicorn?
- Flask alone = single process (not scalable)
- Gunicorn = multiple workers
- Stable, fast, and production-ready

---

## 📂 WSGI File Used

```text
src/
├── app.py        # Flask routes
├── model_loader.py
├── wsgi.py       # WSGI entry for Gunicorn
└── __init__.py

⚙️ Prerequisites

Activate virtual environment:
source .venv/bin/activate

Install dependencies:
pip install gunicorn flask mlflow pandas scikit-learn

▶️ Running the API with Gunicorn

Set environment variables:
export MLFLOW_TRACKING_URI="file:./mlruns"
export RUN_ID=<your_mlflow_run_id>

Start Gunicorn:
gunicorn -w 2 -b 0.0.0.0:6000 src.wsgi:app

What these options mean

-w 2 → 2 worker processes

-b 0.0.0.0:6000 → listen on port 6000

src.wsgi:app → WSGI entry point

🧪 Testing Gunicorn API
Health check

curl http://127.0.0.1:6000/health

Prediction
curl -X POST http://127.0.0.1:6000/predict \
-H "Content-Type: application/json" \
-d '{"MedInc":8.3,"HouseAge":20,"AveRooms":6.0,"AveBedrms":1.1,"Population":300,"AveOccup":3.2,"Latitude":34.2,"Longitude":-118.4}'

VM Deployment Script (deploy.sh)

This script sets up the Housing ML API on an Ubuntu VM using Gunicorn + systemd + Nginx

▶️ How to Run
chmod +x deploy.sh
./deploy.sh

Verify Deployment
curl http://<VM_PUBLIC_IP>/health


Expected response:

{"status":"ok"}

curl -X POST http://<VM_PUBLIC_IP>/predict \
-H "Content-Type: application/json" \
-d '{"MedInc":8.3,"HouseAge":20,"AveRooms":6.0,"AveBedrms":1.1,"Population":300,"AveOccup":3.2,"Latitude":34.2,"Longitude":-118.4}'
