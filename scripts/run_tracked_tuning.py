"""Re-run Module 5's hyperparameter search and log every combination to MLflow."""

from sklearn.linear_model import LinearRegression

from air_quality import data, features, selection, tracking, tuning

ALL_CITIES = ["Kampala", "Nairobi", "Lagos", "Bujumbura"]
EXCLUDED_RAW_COLUMNS = {"id", "site_id", "country", "month"}


def main() -> None:
    """
    Rebuild Module 4's cleaned, RFE-selected dataset, rerun Module 5's
    tune_xgboost grid search, and log every grid point as its own MLflow run.
    """
    # TODO: reuse the Module 2/4/5 functions you already completed —
    # restrict_to_scope (scope to ALL_CITIES and every column except
    # EXCLUDED_RAW_COLUMNS), columns_above_missing_threshold + drop_columns
    # (threshold 0.7), fill_missing_by_city, add_temporal_features,
    # feature_columns, then select_features_rfe (n_features_to_select=8) to
    # get back the same 8 columns as Module 5. Run tune_xgboost with
    # param_grid={"max_depth": [3, 5], "learning_rate": [0.05, 0.2]}, then
    # loop over tuning_result["cv_results"] and call tracking.log_run once
    # per grid point — a short run_name built from combo["params"],
    # params=combo["params"], and metrics={"rmse": combo["rmse"],
    # "mae": combo["mae"], "r2": combo["r2"]} — before printing a short
    # confirmation once every combination has been logged






if __name__ == "__main__":
    main()
