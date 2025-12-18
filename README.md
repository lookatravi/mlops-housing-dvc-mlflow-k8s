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


