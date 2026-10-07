"""Tests for src/air_quality/tuning.py."""

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("xgboost")

from air_quality.tuning import tune_xgboost


def _synthetic_tuning_data() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n_per_group = 30
    parts = []
    for group, offset in [("A", 0.0), ("B", 5.0), ("C", 10.0)]:
        x = rng.normal(size=n_per_group)
        parts.append(
            pd.DataFrame(
                {
                    "group": group,
                    "x": x,
                    "target": offset + 3 * x + rng.normal(scale=0.5, size=n_per_group),
                }
            )
        )
    return pd.concat(parts, ignore_index=True)


def test_tune_xgboost_returns_one_result_per_grid_point():
    df = _synthetic_tuning_data()
    param_grid = {"max_depth": [2, 3], "learning_rate": [0.1, 0.3]}

    result = tune_xgboost(df, feature_cols=["x"], param_grid=param_grid, target_col="target", groups_col="group")

    assert len(result["cv_results"]) == 4
    assert set(result["best_params"].keys()) == {"max_depth", "learning_rate"}
    assert result["best_rmse"] == min(entry["rmse"] for entry in result["cv_results"])
    assert all({"rmse", "mae", "r2"} <= entry.keys() for entry in result["cv_results"])
