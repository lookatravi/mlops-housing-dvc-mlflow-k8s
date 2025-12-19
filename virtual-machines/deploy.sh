#!/bin/bash
set -e

# ====== Config (edit if needed) ======
export APP_DIR=/opt/housing-ml-api
export REPO_URL="https://github.com/lookatravi/mlops-housing-dvc-mlflow-k8s.git"
export APP_USER="ubuntu"
export APP_PORT="6000"

# IMPORTANT: set your MLflow run id (same one you tested)
export RUN_ID="b2f4965e55a447ccb9c4bae8a21e58b0"
export MLFLOW_TRACKING_URI="file:/opt/housing-ml-api/mlruns"

# ====== Setup directory ======
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# ====== Packages ======
apt update -y
apt install -y git python3 python3-venv python3-pip nginx

# ====== Download code ======
if [ ! -d ".git" ]; then
  git clone "$REPO_URL" .
else
  git pull
fi

# ====== Python venv + deps ======
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# Your repo should have requirements.txt. Ensure it includes:
# flask gunicorn mlflow pandas scikit-learn
python3 -m pip install -r requirements.txt

# (Optional) Pull dataset if you want it on VM (only needed for training, not for serving)
# If you use DVC on the VM, install dvc + awscli and run dvc pull.

# ====== systemd: Gunicorn service ======
cat >/etc/systemd/system/housing_gunicorn.service <<EOF
[Unit]
Description=Gunicorn instance for Housing ML API
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
Environment="RUN_ID=$RUN_ID"
Environment="MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI"
ExecStart=$APP_DIR/.venv/bin/gunicorn --workers 2 --bind 127.0.0.1:$APP_PORT src.wsgi:app
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# ====== Nginx reverse proxy ======
cat >/etc/nginx/conf.d/housing_api.conf <<'EOF'
server {
    listen 80;
    server_name _;

    location /health {
        proxy_pass http://127.0.0.1:6000/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /predict {
        proxy_pass http://127.0.0.1:6000/predict;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }
}
EOF

# Remove default nginx site if present
if [ -L /etc/nginx/sites-enabled/default ] || [ -f /etc/nginx/sites-enabled/default ]; then
  rm -f /etc/nginx/sites-enabled/default || true
fi

# ====== Start/enable services ======
systemctl daemon-reload
systemctl enable housing_gunicorn
systemctl restart housing_gunicorn

nginx -t
systemctl enable nginx
systemctl restart nginx

echo "Deployed!"
echo "Try: curl http://<EC2_PUBLIC_IP>/health"
echo "Try: curl -X POST http://<EC2_PUBLIC_IP>/predict -H 'Content-Type: application/json' -d '{\"MedInc\":8.3,\"HouseAge\":20,\"AveRooms\":6.0,\"AveBedrms\":1.1,\"Population\":300,\"AveOccup\":3.2,\"Latitude\":34.2,\"Longitude\":-118.4}'"
