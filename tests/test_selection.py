"""Tests for src/air_quality/selection.py."""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from air_quality.selection import select_features_rfe, select_k_best_features


def _synthetic_selection_data() -> pd.DataFrame:
    rng = np.random.default_rng(0)
    n = 200
    signal = rng.normal(size=n)
    return pd.DataFrame(
        {
            "strong_predictor": signal,
            "weak_predictor": signal * 0.1 + rng.normal(scale=1.0, size=n),
            "pure_noise": rng.normal(size=n),
            "target": signal * 5 + rng.normal(scale=0.1, size=n),
        }
    )


def test_select_k_best_features_keeps_the_most_correlated_column():
    df = _synthetic_selection_data()
    selected = select_k_best_features(
        df, ["strong_predictor", "weak_predictor", "pure_noise"], target_col="target", k=1
    )
    assert selected == ["strong_predictor"]


def test_select_features_rfe_drops_the_uninformative_column():
    df = _synthetic_selection_data()
    selected = select_features_rfe(
        LinearRegression(),
        df,
        ["strong_predictor", "weak_predictor", "pure_noise"],
        target_col="target",
        n_features_to_select=2,
    )
    assert "pure_noise" not in selected
    assert "strong_predictor" in selected
