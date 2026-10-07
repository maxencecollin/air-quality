"""Tests for src/air_quality/features.py."""

import pandas as pd

from air_quality.features import add_temporal_features, feature_columns


def test_add_temporal_features_adds_month_and_dayofweek(sample_two_city_data):
    enriched = add_temporal_features(sample_two_city_data)
    assert "month" in enriched.columns
    assert "dayofweek" in enriched.columns
    expected_month = pd.Timestamp(sample_two_city_data["date"].iloc[0]).month
    assert enriched["month"].iloc[0] == expected_month


def test_feature_columns_excludes_target_and_identifiers(sample_two_city_data):
    enriched = add_temporal_features(sample_two_city_data)
    features = feature_columns(enriched, target_col="pm2_5")
    assert "pm2_5" not in features
    assert "city" not in features
    assert "date" not in features
    assert "month" in features
