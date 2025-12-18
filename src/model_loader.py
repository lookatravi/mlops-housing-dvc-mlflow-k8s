import os
import mlflow.pyfunc

# Set RUN_ID from env, else hardcode once
RUN_ID = os.getenv("RUN_ID", "").strip()

def load_model():
    if not RUN_ID:
        raise RuntimeError("RUN_ID not set. Run: export RUN_ID=<your_run_id>")
    model_uri = f"runs:/{RUN_ID}/model"
    return mlflow.pyfunc.load_model(model_uri)
