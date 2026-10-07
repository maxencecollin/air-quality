"""Tests for src/air_quality/registry.py."""

import pytest

pytest.importorskip("mlflow")

from sklearn.linear_model import LinearRegression, Ridge

from air_quality.registry import load_champion, promote_to_champion, register_pipeline


def test_champion_alias_points_to_the_promoted_version(tmp_path):
    tracking_uri = f"file:{tmp_path / 'mlruns'}"

    linear = LinearRegression()
    ridge = Ridge()

    version_1 = register_pipeline(linear, "test_model", tracking_uri=tracking_uri)
    version_2 = register_pipeline(ridge, "test_model", tracking_uri=tracking_uri)

    promote_to_champion("test_model", version_1, tracking_uri=tracking_uri)
    assert isinstance(load_champion("test_model", tracking_uri=tracking_uri), LinearRegression)

    promote_to_champion("test_model", version_2, tracking_uri=tracking_uri)
    assert isinstance(load_champion("test_model", tracking_uri=tracking_uri), Ridge)
