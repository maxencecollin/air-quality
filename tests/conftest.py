"""Shared fixtures for the Air Quality test suite."""

import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def sample_two_city_data() -> pd.DataFrame:
    """Small synthetic dataset spanning two cities, with some missing values."""
    rng = np.random.default_rng(0)
    dates = pd.date_range("2023-01-01", periods=20, freq="D")

    rows = []
    for city, lat, lon in [("CityA", 1.0, 30.0), ("CityB", -1.0, 36.0)]:
        for date in dates:
            rows.append(
                {
                    "city": city,
                    "date": date,
                    "hour": 12,
                    "site_latitude": lat,
                    "site_longitude": lon,
                    "pm2_5": rng.normal(25, 10),
                    "sulphurdioxide_so2_column_number_density": rng.normal(0, 1),
                }
            )

    df = pd.DataFrame(rows)
    df.loc[0:2, "sulphurdioxide_so2_column_number_density"] = np.nan
    return df
