"""Data loading and cleaning utilities for the Air Quality pipeline."""

from pathlib import Path

import pandas as pd

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_datasets(data_dir: Path = DEFAULT_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the raw train and test CSV files.

    Parameters:
    - data_dir: directory containing train.csv and test.csv

    Returns:
    - (train_df, test_df): the two DataFrames, loaded as-is
    """
    # TODO: read train.csv and test.csv from data_dir with pd.read_csv, and
    # return them as a (train_df, test_df) tuple


def restrict_to_scope(
    df: pd.DataFrame,
    cities: list[str],
    columns: list[str],
    max_rows_per_city: int | None = None,
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Keep only the given cities and columns, optionally capping rows per city.

    Parameters:
    - df: DataFrame to restrict
    - cities: list of city names to keep
    - columns: list of column names to keep
    - max_rows_per_city: if given, randomly sample at most this many rows per city
    - random_state: seed used for the random sample, so results are reproducible

    Returns:
    - DataFrame filtered to the given cities and columns, index reset
    """
    # TODO: filter df to the given cities and columns, then, if max_rows_per_city
    # is set, draw a reproducible random sample of at most that many rows for
    # each city and concatenate the results back into a single DataFrame




def fill_missing_by_city(
    df: pd.DataFrame,
    columns: list[str],
    city_col: str = "city",
    date_col: str = "date",
) -> pd.DataFrame:
    """
    Forward/backward-fill the given columns within each city, ordered by date.

    Parameters:
    - df: DataFrame to fill
    - columns: list of column names to fill
    - city_col: column identifying the city, used to group rows
    - date_col: column used to sort rows within each city before filling

    Returns:
    - DataFrame with the given columns filled, one city at a time
    """
    # TODO: sort by city_col and date_col, then for each column, group by
    # city_col and apply forward-fill followed by backward-fill within each
    # group with groupby().transform() — never fill across cities


# ============================================================================
# Session 3 — optional modules (not needed for Session 2's practical_3)
# ============================================================================

# --- Module 2: Advanced cleaning (content/session3/practical_2) ---


def columns_above_missing_threshold(df: pd.DataFrame, threshold: float = 0.7) -> list[str]:
    """
    Return columns whose missing-value ratio exceeds the threshold.

    Parameters:
    - df: DataFrame to inspect
    - threshold: fraction of missing values (between 0 and 1) above which a
      column is reported

    Returns:
    - list of column names whose missing-value ratio is strictly above threshold
    """
    # TODO: compute the fraction of missing values per column, then return the
    # names of the columns whose fraction is strictly above threshold


def drop_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Drop the given columns if present.

    Parameters:
    - df: DataFrame to drop columns from
    - columns: list of column names to drop; names not present in df are ignored

    Returns:
    - DataFrame without the given columns
    """
    # TODO: drop the given columns from df, ignoring any name that is not
    # actually a column of df
