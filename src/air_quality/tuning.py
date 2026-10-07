"""Hyperparameter tuning utilities for the Air Quality pipeline.

xgboost is an optional dependency (the "ml" group in pyproject.toml) — it is
imported lazily inside tune_xgboost, not at module load time, so importing
this module never requires it to be installed.
"""

import pandas as pd
from sklearn.model_selection import GridSearchCV, GroupKFold


def tune_xgboost(
    df: pd.DataFrame,
    feature_cols: list[str],
    param_grid: dict[str, list],
    target_col: str = "pm2_5",
    groups_col: str = "city",
) -> dict:
    """
    Tune XGBRegressor hyperparameters with GridSearchCV, using GroupKFold
    (one fold per distinct value of groups_col) as the cross-validation
    strategy — the same guarantee as Module 3's evaluate_group_cv (a group
    never appears in both train and validation for a given fold), applied
    through scikit-learn's own tuning tool instead of a hand-rolled loop.

    Every grid point is scored on rmse, mae and r2 together — the same three
    metrics regression_metrics() always reports — even though only rmse
    decides which combination counts as "best".

    Parameters:
    - df: DataFrame containing feature_cols, target_col and groups_col
    - feature_cols: list of column names used as input features
    - param_grid: dict mapping XGBRegressor parameter names to lists of
      values to try, e.g. {"max_depth": [3, 5], "learning_rate": [0.05, 0.2]}
    - target_col: name of the column to predict
    - groups_col: column identifying each row's group (e.g. "city")

    Returns:
    - dict with "best_params" (the grid point with lowest RMSE), "best_rmse",
      and "cv_results" (one {"params", "rmse", "mae", "r2"} entry per grid point)
    """
    # TODO: run GridSearchCV(XGBRegressor(n_estimators=100, random_state=42),
    # param_grid, cv=GroupKFold(n_splits=df[groups_col].nunique()), scoring={
    # "rmse": "neg_root_mean_squared_error", "mae": "neg_mean_absolute_error",
    # "r2": "r2"}, refit="rmse") — refit picks the best combination by rmse,
    # but every combination still gets all three metrics recorded in
    # grid.cv_results_["mean_test_rmse"/"mean_test_mae"/"mean_test_r2"]. Fit
    # it passing groups=df[groups_col], then build the return dict from
    # grid.best_params_/grid.best_score_/grid.cv_results_ (rmse/mae come back
    # negative from "neg_..." scorers — negate them back to plain values; r2
    # does not need negating)


