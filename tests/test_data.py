"""Tests for src/air_quality/data.py (Session 2 scope only — see test_data_advanced.py
for the Session 3 "advanced cleaning" module's functions)."""

from air_quality.data import fill_missing_by_city, restrict_to_scope


def test_restrict_to_scope_filters_cities_and_columns(sample_two_city_data):
    scoped = restrict_to_scope(
        sample_two_city_data, cities=["CityA"], columns=["city", "date", "pm2_5"]
    )
    assert set(scoped["city"].unique()) == {"CityA"}
    assert list(scoped.columns) == ["city", "date", "pm2_5"]


def test_restrict_to_scope_caps_rows_per_city(sample_two_city_data):
    scoped = restrict_to_scope(
        sample_two_city_data,
        cities=["CityA", "CityB"],
        columns=["city", "date", "pm2_5"],
        max_rows_per_city=5,
    )
    assert scoped["city"].value_counts().to_dict() == {"CityA": 5, "CityB": 5}


def test_fill_missing_by_city_does_not_mix_cities(sample_two_city_data):
    df = sample_two_city_data.copy()
    df.loc[df["city"] == "CityA", "sulphurdioxide_so2_column_number_density"] = None

    filled = fill_missing_by_city(df, columns=["sulphurdioxide_so2_column_number_density"])

    city_a_values = filled.loc[filled["city"] == "CityA", "sulphurdioxide_so2_column_number_density"]
    city_b_values = filled.loc[filled["city"] == "CityB", "sulphurdioxide_so2_column_number_density"]
    assert city_a_values.isna().all()
    assert not city_b_values.isna().any()
