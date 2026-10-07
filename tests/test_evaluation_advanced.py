"""Tests for the Session 3 "robust evaluation" module's functions in
src/air_quality/evaluation.py. Not part of Session 2's practical_3 scope — see
content/session3/practical_3 (robust evaluation) once that module is built."""

import pandas as pd
from sklearn.dummy import DummyRegressor

from air_quality.evaluation import evaluate_group_cv


def test_evaluate_group_cv_has_one_fold_per_group(sample_two_city_data):
    result = evaluate_group_cv(
        DummyRegressor(strategy="mean"),
        sample_two_city_data,
        feature_cols=["sulphurdioxide_so2_column_number_density"],
        groups_col="city",
    )

    assert len(result["folds"]) == 2
    assert {fold["test_group"] for fold in result["folds"]} == {"CityA", "CityB"}
    assert all({"rmse", "mae", "r2"} <= fold.keys() for fold in result["folds"])


def test_evaluate_group_cv_aggregates_metrics_across_folds():
    df = pd.DataFrame(
        {
            "group": ["A", "A", "B", "B"],
            "x": [0, 0, 0, 0],
            "pm2_5": [10.0, 10.0, 20.0, 20.0],
        }
    )

    # Each fold trains on the other, constant group: predicting its mean gives
    # exactly the same error (10) on both folds, so mean == that value and std == 0.
    result = evaluate_group_cv(DummyRegressor(strategy="mean"), df, feature_cols=["x"], groups_col="group")

    assert result["rmse_mean"] == 10.0
    assert result["rmse_std"] == 0.0
    assert result["mae_mean"] == 10.0
