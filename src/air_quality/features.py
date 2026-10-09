"""Feature engineering utilities for the Air Quality pipeline."""

import pandas as pd


def add_temporal_features(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    """
    Add month and day-of-week features extracted from the date column.

    Parameters:
    - df: DataFrame containing date_col
    - date_col: name of the column to parse as a date

    Returns:
    - copy of df with two extra columns, "month" and "dayofweek"
    """
    enriched = df.copy()
    enriched[date_col] = pd.to_datetime(enriched[date_col])
    enriched["month"] = enriched[date_col].dt.month
    enriched["dayofweek"] = enriched[date_col].dt.dayofweek
    return enriched


def feature_columns(df: pd.DataFrame, target_col: str = "pm2_5") -> list[str]:
    """
    List the numeric columns usable as model features.

    Excludes site_latitude/site_longitude: within a single city these vary only
    slightly around the local monitoring sites, so a linear model fits a huge
    coefficient on them and the prediction explodes once evaluated on a city with
    very different coordinates. City-level geography is handled through the
    train/test city split itself, not as a raw numeric feature, at this stage.

    Parameters:
    - df: DataFrame to inspect
    - target_col: name of the target column, excluded from the result

    Returns:
    - list of numeric column names, excluding target_col, "city", "date",
      "site_latitude" and "site_longitude"
    """
    excluded = {target_col, "city", "date", "site_latitude", "site_longitude"}
    return [col for col in df.select_dtypes(include="number").columns if col not in excluded]
