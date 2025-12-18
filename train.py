from __future__ import annotations
import os, argparse, math
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn

def parse_args():
    p = argparse.ArgumentParser("MLflow demo (California Housing)")
    p.add_argument("--csv", default="data/housing.csv")
    p.add_argument("--target", default="MedHouseVal")
    p.add_argument("--experiment", default="housing-prediction")
    p.add_argument("--run", default="run-1")
    p.add_argument("--n-estimators", type=int, default=200)
    p.add_argument("--max-depth", type=int, default=12)
    p.add_argument("--test-size", type=float, default=0.2)
    p.add_argument("--random-state", type=int, default=42)
    return p.parse_args()

def main():
    args = parse_args()

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(args.experiment)

    df = pd.read_csv(args.csv)
    X = df.drop(columns=[args.target])
    y = df[args.target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state
    )

    with mlflow.start_run(run_name=args.run):
        mlflow.log_params({
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "test_size": args.test_size,
            "random_state": args.random_state,
            "train_rows": len(X_train),
            "test_rows": len(X_test),
        })

        model = RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=args.random_state,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        rmse = float(math.sqrt(mse))
        r2 = float(r2_score(y_test, preds))

        mlflow.log_metrics({"mse": float(mse), "rmse": rmse, "r2": r2})
        mlflow.sklearn.log_model(model, name="model")

        print(f"✅ Done. rmse={rmse:.4f} r2={r2:.4f}")

if __name__ == "__main__":
    main()
