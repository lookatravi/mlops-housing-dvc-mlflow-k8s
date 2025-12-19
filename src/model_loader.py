import os
from pathlib import Path
import mlflow.pyfunc

def load_model():
    model_path = os.getenv("MODEL_PATH", "").strip()
    if not model_path:
        raise RuntimeError("MODEL_PATH not set. Set it in systemd Environment=MODEL_PATH=...")

    p = Path(model_path)
    if not p.exists():
        raise RuntimeError(f"MODEL_PATH does not exist: {p}")

    # model_path should point to the folder that contains MLmodel
    # e.g. .../artifacts
    mlmodel_file = p / "MLmodel"
    if not mlmodel_file.exists():
        raise RuntimeError(f"MLmodel not found under MODEL_PATH: {mlmodel_file}")

    model = mlflow.pyfunc.load_model(str(p))
    if model is None:
        raise RuntimeError("mlflow.pyfunc.load_model returned None (unexpected)")

    return model
