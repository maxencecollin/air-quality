"""End-to-end test for src/air_quality/workflows.py, against the real dataset.

run_advanced (Session 3) is intentionally not tested here: students write and
grow it themselves one optional module at a time, so there is no single fixed
shape a test could check. See src/air_quality/workflows.py's docstring."""

from air_quality.workflows import PipelineConfig, run_baseline


def test_run_baseline_returns_finite_metrics():
    metrics = run_baseline(PipelineConfig(max_rows_per_city=200))
    assert set(metrics) == {"rmse", "mae", "r2"}
    assert metrics["rmse"] >= 0
