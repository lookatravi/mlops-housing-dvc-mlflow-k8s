import os
import mlflow
import mlflow.pyfunc

def load_model():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
    mlflow.set_tracking_uri(tracking_uri)

    run_id = os.getenv("RUN_ID")

    # 1️⃣ If RUN_ID is explicitly provided (prod / rollback)
    if run_id:
        model_uri = f"runs:/{run_id}/model"
        return mlflow.pyfunc.load_model(model_uri)

    # 2️⃣ Otherwise auto-pick latest successful run
    experiments = mlflow.search_experiments()
    if not experiments:
        raise RuntimeError("No MLflow experiments found")

    experiment_id = experiments[0].experiment_id

    runs = mlflow.search_runs(
        experiment_ids=[experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1,
    )

    if runs.empty:
        raise RuntimeError("No MLflow runs found")

    latest_run_id = runs.iloc[0].run_id
    model_uri = f"runs:/{latest_run_id}/model"

    print(f"Loaded latest MLflow model from run_id={latest_run_id}")

    return mlflow.pyfunc.load_model(model_uri)
