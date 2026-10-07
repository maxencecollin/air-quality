"""Model registry utilities for the Air Quality pipeline.

mlflow is an optional dependency (the "mlops" group in pyproject.toml) — it is
imported lazily inside each function, not at module load time, so importing
this module never requires it to be installed.
"""

from pathlib import Path

# Anchored to this file, not the current working directory — same principle
# as data.py's DEFAULT_DATA_DIR. A relative "file:./mlruns" would point
# somewhere different depending on whether it's resolved from a script run
# from the project root or a notebook whose kernel cwd is its own folder;
# this always resolves to air_quality/mlruns, the same store
# scripts/run_tracked_tuning.py (Module 6) already writes to.
DEFAULT_TRACKING_URI = f"file:{Path(__file__).resolve().parents[2] / 'mlruns'}"


def register_pipeline(
    pipeline,
    model_name: str,
    tracking_uri: str = DEFAULT_TRACKING_URI,
    experiment_name: str = "air_quality",
) -> str:
    """
    Log a fitted pipeline and register it as a new version of a named model.

    Parameters:
    - pipeline: a fitted scikit-learn estimator or Pipeline to log
    - model_name: name of the registered model this becomes a new version
      of (created automatically the first time this name is used)
    - tracking_uri: where MLflow stores runs and the model registry; the
      default writes to a local ./mlruns folder, no server required
    - experiment_name: groups the logging run under this experiment

    Returns:
    - the new version number, as a string (e.g. "1", "2", ...)
    """
    # TODO: import mlflow, call mlflow.set_tracking_uri(tracking_uri) and
    # mlflow.set_experiment(experiment_name), then open mlflow.start_run()
    # as a context manager and call mlflow.sklearn.log_model(pipeline,
    # name="model", registered_model_name=model_name) inside it; return
    # str(model_info.registered_model_version)




def promote_to_champion(model_name: str, version: str, tracking_uri: str = DEFAULT_TRACKING_URI) -> None:
    """
    Point the "champion" alias at a specific registered model version — the
    one calling code is meant to load and use. Moving the alias to a
    different version later requires no change to any code that loads by
    alias (see load_champion).

    Parameters:
    - model_name: name of the registered model
    - version: version number to promote, as returned by register_pipeline
    - tracking_uri: must match whatever register_pipeline used

    Returns:
    - None
    """
    # TODO: import mlflow, call mlflow.set_tracking_uri(tracking_uri), then
    # mlflow.MlflowClient().set_registered_model_alias(model_name,
    # "champion", version)



def load_champion(model_name: str, tracking_uri: str = DEFAULT_TRACKING_URI):
    """
    Load whichever registered model version currently holds the "champion"
    alias. Calling code never needs to know a run ID or version number —
    only the model name.

    Parameters:
    - model_name: name of the registered model
    - tracking_uri: must match whatever register_pipeline/promote_to_champion used

    Returns:
    - the loaded model or pipeline, ready to call .predict() on
    """
    # TODO: import mlflow, call mlflow.set_tracking_uri(tracking_uri), then
    # return mlflow.sklearn.load_model(f"models:/{model_name}@champion")

