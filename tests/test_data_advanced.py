"""Tests for the Session 3 "advanced cleaning" module's functions in
src/air_quality/data.py. Not part of Session 2's practical_3 scope — see
content/session3/practical_2 (advanced cleaning) once that module is built."""

from air_quality.data import columns_above_missing_threshold, drop_columns


def test_columns_above_missing_threshold_depends_on_threshold(sample_two_city_data):
    df = sample_two_city_data.copy()
    df["half_missing"] = None
    df.loc[df.index[::2], "half_missing"] = 1.0

    assert "half_missing" in columns_above_missing_threshold(df, threshold=0.4)
    assert "half_missing" not in columns_above_missing_threshold(df, threshold=0.6)


def test_drop_columns_removes_only_requested_columns(sample_two_city_data):
    dropped = drop_columns(sample_two_city_data, ["hour"])
    assert "hour" not in dropped.columns
    assert "pm2_5" in dropped.columns
