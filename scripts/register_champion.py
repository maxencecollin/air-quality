"""Register two versions of Module 7's pipeline and promote the better one to champion."""

from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.pipeline import Pipeline

from air_quality import data, features, registry
from air_quality.transformers import AirQualityCleaner

ALL_CITIES = ["Kampala", "Nairobi", "Lagos", "Bujumbura"]
EXCLUDED_RAW_COLUMNS = {"id", "site_id", "country", "month"}
MODEL_NAME = "air_quality_model"


def main() -> None:
    """
    Rebuild Module 7's chained Pipeline (AirQualityCleaner + RFE + a model)
    twice, once with LinearRegression and once with Ridge, register each as
    a new version of MODEL_NAME, and promote whichever one scores better on
    cross_val_score to the "champion" alias.
    """
    # TODO: reuse the Module 2/4 functions you already completed —
    # restrict_to_scope (scope to ALL_CITIES and every column except
    # EXCLUDED_RAW_COLUMNS) and add_temporal_features — to rebuild enriched
    # on the wide scope. For each of LinearRegression and Ridge: build
    # Pipeline([("cleaner", AirQualityCleaner(missing_threshold=0.6)),
    # ("selector", RFE(estimator=<a fresh instance>, n_features_to_select=8)),
    # ("model", <a fresh instance>)]) — two separate instances of the same
    # class, not one shared object. Evaluate it with cross_val_score(...,
    # groups=enriched["city"], cv=GroupKFold(n_splits=4),
    # scoring="neg_root_mean_squared_error") to get a comparable rmse_mean,
    # then fit the pipeline on the *entire* enriched dataset
    # (pipeline.fit(enriched, enriched["pm2_5"])) before registering it with
    # registry.register_pipeline(pipeline, MODEL_NAME) — cross_val_score
    # only estimates performance, the registered version should be trained
    # on everything you trust that estimate to generalize from. Keep each
    # version's rmse_mean, then call
    # registry.promote_to_champion(MODEL_NAME, <the better version>) for
    # whichever one scored lower, and print a short summary of both
    # candidates and which one won.





if __name__ == "__main__":
    main()
