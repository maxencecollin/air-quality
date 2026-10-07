"""Feature selection utilities for the Air Quality pipeline."""

import pandas as pd
from sklearn.feature_selection import RFE, SelectKBest, f_regression


def select_k_best_features(
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "pm2_5",
    k: int = 8,
) -> list[str]:
    """
    Rank features independently by their univariate relationship with the
    target, and return the k highest-scoring ones. Because each feature is
    scored on its own, two features carrying the exact same information can
    both be selected — this method has no way to notice the redundancy.

    Parameters:
    - df: DataFrame containing feature_cols and target_col
    - feature_cols: candidate column names to rank
    - target_col: name of the column to predict
    - k: number of features to keep

    Returns:
    - list of the k selected column names, in their original order in feature_cols
    """
    # TODO: fit SelectKBest(score_func=f_regression, k=k) on df[feature_cols]
    # and df[target_col], then use its get_support() boolean mask to return
    # the corresponding names from feature_cols


def select_features_rfe(
    model,
    df: pd.DataFrame,
    feature_cols: list[str],
    target_col: str = "pm2_5",
    n_features_to_select: int = 8,
) -> list[str]:
    """
    Rank features by recursively fitting model on the current set and dropping
    the least important one, one at a time, until n_features_to_select remain.
    Because each step refits on the features still in the running, a feature
    that is redundant given another one already kept contributes little to the
    fit and tends to be eliminated — unlike select_k_best_features, which
    cannot see that kind of redundancy.

    Parameters:
    - model: a scikit-learn estimator exposing coef_ or feature_importances_
      after fitting (e.g. LinearRegression); RFE fits a fresh clone internally
      at each step
    - df: DataFrame containing feature_cols and target_col
    - feature_cols: candidate column names to rank
    - target_col: name of the column to predict
    - n_features_to_select: number of features to keep

    Returns:
    - list of the selected column names, in their original order in feature_cols
    """
    # TODO: fit RFE(estimator=model, n_features_to_select=n_features_to_select)
    # on df[feature_cols] and df[target_col], then use its get_support()
    # boolean mask the same way as select_k_best_features
