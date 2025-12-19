import os
import mlflow
import mlflow.pyfunc

def load_model():
    # Ensure correct tracking URI
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "file:/opt/housing-ml-api/mlruns")
    mlflow.set_tracking_uri(tracking_uri)

    # 1️⃣ If RUN_ID is provided (production / rollback)
    run_id = os.getenv("RUN_ID")
    if run_id:
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.pyfunc.load_model(model_uri)
        return model

    # 2️⃣ Otherwise load latest run from the ONLY experiment
    experiments = mlflow.search_experiments()
    if not experiments:
        raise RuntimeError("No MLflow experiments found")

    # you have only ONE real experiment → use the latest
    experiment_id = experiments[-1].experiment_id

    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise RuntimeError("No MLflow runs found in experiment")

    latest_run_id = runs.iloc[0].run_id
    model_uri = f"runs:/{latest_run_id}/model"

    print(f"Loaded MLflow model from run_id={latest_run_id}")

    model = mlflow.pyfunc.load_model(model_uri)
    return model
