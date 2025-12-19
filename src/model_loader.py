import os
import mlflow.pyfunc

def load_model():
    run_id = os.getenv("RUN_ID")
    if not run_id:
        raise RuntimeError("RUN_ID is required for inference")

    model_uri = f"runs:/{run_id}/model"
    return mlflow.pyfunc.load_model(model_uri)
