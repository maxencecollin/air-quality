"""End-to-end workflow assembling the base Air Quality pipeline."""

from dataclasses import dataclass, field

from sklearn.linear_model import LinearRegression

from air_quality import data, evaluation, features

DEFAULT_COLUMNS = [
    "city",
    "date",
    "hour",
    "site_latitude",
    "site_longitude",
    "pm2_5",
    "sulphurdioxide_so2_column_number_density",
    "carbonmonoxide_co_column_number_density",
    "nitrogendioxide_no2_column_number_density",
    "formaldehyde_tropospheric_hcho_column_number_density",
    "uvaerosolindex_absorbing_aerosol_index",
    "ozone_o3_column_number_density",
    "uvaerosollayerheight_aerosol_height",
    "cloud_cloud_fraction",
]


@dataclass
class PipelineConfig:
    """Settings for run_baseline: which cities, which columns, how much data."""

    train_city: str = "Kampala"
    test_city: str = "Nairobi"
    columns: list[str] = field(default_factory=lambda: list(DEFAULT_COLUMNS))
    max_rows_per_city: int = 1200
    random_state: int = 42


def run_baseline(config: PipelineConfig | None = None) -> dict[str, float]:
    """
    Load, clean, split by city, engineer features, train and evaluate a linear baseline.

    Parameters:
    - config: pipeline settings; a default PipelineConfig() is used if omitted

    Returns:
    - dict of regression metrics (see evaluation.regression_metrics)
    """
    config = config or PipelineConfig()
    train_df, _ = data.load_datasets()
    cities = [config.train_city, config.test_city]

    scoped = data.restrict_to_scope(
        train_df, cities, config.columns, config.max_rows_per_city, config.random_state
    )
    fillable_columns = [c for c in config.columns if c not in ("city", "date")]
    cleaned = data.fill_missing_by_city(scoped, fillable_columns)
    enriched = features.add_temporal_features(cleaned)

    train_split = enriched[enriched["city"] == config.train_city]
    test_split = enriched[enriched["city"] == config.test_city]

    feature_cols = features.feature_columns(enriched)
    model = LinearRegression()
    return evaluation.evaluate_manual_split(model, train_split, test_split, feature_cols)


# ============================================================================
# Session 3 — optional modules (not needed for Session 2's practical_3)
# ============================================================================


@dataclass
class AdvancedPipelineConfig:
    """
    Settings for run_advanced. Starts with what Module 2 needs; later modules may
    add or remove fields here as your pipeline evolves — see each module's page
    under content/session3/ for what changes.
    """

    train_city: str = "Kampala"
    test_city: str = "Bujumbura"
    cities: list[str] = field(
        default_factory=lambda: ["Kampala", "Nairobi", "Lagos", "Bujumbura"]
    )
    columns: list[str] = field(default_factory=lambda: list(DEFAULT_COLUMNS))
    missing_threshold: float = 0.7


def run_advanced(config: AdvancedPipelineConfig | None = None) -> dict:
    """
    The Session 3 pipeline: starts where run_baseline stops, and grows one optional
    module at a time. Each module you complete under content/session3/ tells you
    exactly what to add or change here — this function is yours to write and
    maintain, not something given to you complete.

    There is deliberately no automated test for it: its correct shape depends on
    which optional modules you have added, something no fixed test could know in
    advance. Verify it by calling it from a notebook or a Python shell and
    checking that the printed metrics make sense for whatever you have built so far.

    Parameters:
    - config: pipeline settings; a default AdvancedPipelineConfig() is used if omitted

    Returns:
    - dict of metrics — the exact shape depends on which modules you have added
    """
    # TODO: build this up module by module, following content/session3/'s pages
