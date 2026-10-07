"""Tests for src/air_quality/transformers.py."""

import pandas as pd

from air_quality.transformers import AirQualityCleaner


def _make_frame(city_missing_ratio: dict) -> pd.DataFrame:
    """Small frame where "flaky" is missing at the given ratio per city
    (its first rows, chronologically) and "reliable" is never missing."""
    dates = pd.date_range("2023-01-01", periods=10, freq="D")
    rows = []
    for city, missing_ratio in city_missing_ratio.items():
        n_missing = round(missing_ratio * len(dates))
        for i, date in enumerate(dates):
            rows.append(
                {
                    "city": city,
                    "date": date,
                    "reliable": float(i),
                    "flaky": None if i < n_missing else float(i),
                    "pm2_5": float(i),
                }
            )
    return pd.DataFrame(rows)


def test_fit_learns_the_drop_decision_only_from_the_data_it_is_given():
    # "flaky" is 100% missing in the fit data -> learned as "drop"
    fit_data = _make_frame({"CityA": 1.0, "CityB": 1.0})
    cleaner = AirQualityCleaner(missing_threshold=0.5).fit(fit_data)
    assert "flaky" in cleaner.columns_to_drop_

    # transform data where "flaky" is NOT missing at all -- the frozen
    # decision must still drop it; transform must not recompute from scratch
    transform_data = _make_frame({"CityC": 0.0})
    result = cleaner.transform(transform_data)
    assert "flaky" not in result.columns
    assert "reliable" in result.columns


def test_transform_fills_remaining_missing_values_per_city():
    df = _make_frame({"CityA": 0.3, "CityB": 0.3})
    cleaner = AirQualityCleaner(missing_threshold=0.9).fit(df)  # 0.3 < 0.9, "flaky" stays
    result = cleaner.transform(df)

    assert "flaky" in result.columns
    assert result["flaky"].isna().sum() == 0
