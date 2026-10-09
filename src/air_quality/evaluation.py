"""Evaluation utilities for the Air Quality pipeline."""

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold


def regression_metrics(y_true, y_pred) -> dict[str, float]:
    """
    Compute RMSE, MAE and R2 for a set of predictions.

    Parameters:
    - y_true: true target values
    - y_pred: predicted target values, same length as y_true

    Returns:
    - dict with keys "rmse", "mae", "r2"
    """
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def evaluate_manual_split(
    model,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "pm2_5",
) -> dict[str, float]:
    """
    Fit a model on train_df and evaluate it on test_df (a different city).

    Parameters:
    - model: a scikit-learn estimator, following the fit/predict contract
    - train_df: DataFrame used to fit the model
    - test_df: DataFrame used to evaluate the model (a city train_df has not seen)
    - feature_cols: list of column names used as input features
    - target_col: name of the column to predict

    Returns:
    - dict of regression metrics (see regression_metrics), computed on test_df
    """
    model.fit(train_df[feature_cols], train_df[target_col])
    y_pred = model.predict(test_df[feature_cols])
    return regression_metrics(test_df[target_col], y_pred)


# ============================================================================
# Session 3 — optional modules (not needed for Session 2's practical_3)
# ============================================================================

# --- Module 3: Robust evaluation (content/session3/practical_3) ---


def evaluate_group_cv(
    model,
    df: pd.DataFrame,
    feature_cols: list[str],
    groups_col: str = "city",
    target_col: str = "pm2_5",
) -> dict:
    """
    Evaluate a model with GroupKFold, holding out one group at a time.

    Generalizes evaluate_manual_split's single train/test pair to every group in
    df: with as many folds as there are distinct values of groups_col, each fold
    leaves one entire group out for validation and trains on the rest — the same
    guarantee (a group's rows never appear in both train and validation) applied
    systematically instead of to a single manually chosen pair.

    Parameters:
    - model: a scikit-learn estimator, following the fit/predict contract; a
      fresh clone() is fitted for each fold so folds cannot leak state into
      one another
    - df: DataFrame containing feature_cols, target_col and groups_col
    - feature_cols: list of column names used as input features
    - groups_col: column identifying each row's group (e.g. "city")
    - target_col: name of the column to predict

    Returns:
    - dict with "folds" (one dict per fold, each with "test_group" and that
      fold's regression metrics) and "rmse_mean"/"rmse_std"/"mae_mean"/
      "mae_std"/"r2_mean"/"r2_std" aggregated across folds
    """
    # TODO: run GroupKFold with one fold per distinct value of groups_col (so
    # each fold holds out exactly one group), fit a fresh clone() of model on
    # each fold's training rows, evaluate it on the held-out group with
    # regression_metrics, then aggregate the mean and std of each metric
    # across folds




