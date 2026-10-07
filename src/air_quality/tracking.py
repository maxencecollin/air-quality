"""Experiment tracking utilities for the Air Quality pipeline.

mlflow is an optional dependency (the "mlops" group in pyproject.toml) — it is
imported lazily inside log_run, not at module load time, so importing this
module never requires it to be installed.
"""


def log_run(
    run_name: str,
    params: dict,
    metrics: dict,
    tracking_uri: str = "file:./mlruns",
    experiment_name: str = "air_quality",
) -> str:
    """
    Log one experiment run to MLflow: its parameters (whatever describes the
    configuration you ran — e.g. missing_threshold, k, max_depth) and the
    resulting metrics (must be a flat dict of numbers — flatten a nested
    result like run_advanced's "folds" list into individual metric names
    yourself before calling this).

    Parameters:
    - run_name: a short, descriptive label for this run (shown in the MLflow UI)
    - params: dict of run configuration values, logged as MLflow params
    - metrics: flat dict of numeric results, logged as MLflow metrics
    - tracking_uri: where MLflow stores runs; the default writes to a local
      ./mlruns folder, no server required
    - experiment_name: groups related runs together in the MLflow UI

    Returns:
    - the MLflow run ID
    """
    # TODO: import mlflow, call mlflow.set_tracking_uri(tracking_uri) and
    # mlflow.set_experiment(experiment_name), then open
    # mlflow.start_run(run_name=run_name) as a context manager, log_params(params)
    # and log_metrics(metrics) inside it, and return run.info.run_id


