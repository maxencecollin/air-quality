"""Tests for src/air_quality/tracking.py."""

import pytest

pytest.importorskip("mlflow")

from air_quality.tracking import log_run


def test_log_run_stores_params_and_metrics(tmp_path):
    import mlflow

    tracking_uri = f"file:{tmp_path / 'mlruns'}"
    run_id = log_run(
        run_name="test_run",
        params={"missing_threshold": 0.7},
        metrics={"rmse_mean": 27.6},
        tracking_uri=tracking_uri,
    )

    mlflow.set_tracking_uri(tracking_uri)
    run = mlflow.get_run(run_id)

    assert run.data.params["missing_threshold"] == "0.7"
    assert run.data.metrics["rmse_mean"] == 27.6
