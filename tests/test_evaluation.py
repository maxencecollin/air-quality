"""Tests for src/air_quality/evaluation.py."""

import numpy as np
import pandas as pd

from air_quality.evaluation import evaluate_manual_split, regression_metrics


def test_regression_metrics_perfect_prediction_has_zero_error():
    y_true = np.array([1.0, 2.0, 3.0])
    metrics = regression_metrics(y_true, y_true)
    assert metrics["rmse"] == 0
    assert metrics["mae"] == 0
    assert metrics["r2"] == 1


class _ConstantModel:
    """Predicts the train-set mean, regardless of features."""

    def fit(self, X, y):
        self._mean = y.mean()

    def predict(self, X):
        return np.full(len(X), self._mean)


def test_evaluate_manual_split_fits_on_train_and_scores_on_test():
    train_df = pd.DataFrame({"x": [1, 2, 3], "pm2_5": [10.0, 20.0, 30.0]})
    test_df = pd.DataFrame({"x": [1, 2], "pm2_5": [15.0, 15.0]})

    metrics = evaluate_manual_split(_ConstantModel(), train_df, test_df, feature_cols=["x"])

    assert metrics["mae"] == 5.0
