# Module 3 — Transfer to Python

## Why a notebook alone is not enough

1. **Hidden state and execution order.** A notebook depends on which cells were run, in what order, and what is still in memory. In `02_pipeline.ipynb`, `train_df` only has `month`/`dayofweek` if the step 4 cell ran after step 3, and `feature_cols` from step 5 is silently reused by the "Going further" cell. A function in `src/air_quality/` receives everything as parameters and returns its result, so it behaves the same every time it is called.
2. **Reuse without copy-paste.** In the notebook, the fit/predict/metrics code is written once in step 5 and then rewritten as an `evaluate` helper for the reversed split. Every new experiment (another city, another model) means copying cells again. In a module, `evaluation.evaluate_manual_split` is written once and imported from the notebook, a script, or Session 3 code.
3. **Automated tests.** A notebook is checked by eye: re-run it and look at the output. With functions in `src/`, `pytest` checks each behaviour on its own (e.g. that `fill_missing_by_city` never fills one city with another city's values), in seconds, after every change. A regression is caught immediately instead of noticed later in a plot.
4. **Running outside Jupyter.** `scripts/run_pipeline.py --train-city Nairobi --test-city Kampala` runs the whole pipeline from the command line, with no kernel and no manual clicks. The same entry point can be used by a scheduled job, CI, or a colleague who never opens the notebook.
5. **Reviewable version control.** A `.ipynb` file is JSON mixed with base64 images and execution counts: a one-line change produces a large, unreadable diff. A `.py` file gives clean diffs, so each commit shows exactly which function changed and why.

## What a `dataclass` is, and what it saves for `PipelineConfig`

A `dataclass` is a class decorated with `@dataclass`: from a list of typed attributes with default values, Python generates the usual boilerplate methods. For `PipelineConfig`, it writes for us:
- `__init__`, which takes `train_city`, `test_city`, `columns`, `max_rows_per_city` and `random_state` as arguments (with their defaults) and assigns each one to `self`;
- `__repr__`, so printing a config shows all its values (`PipelineConfig(train_city='Kampala', ...)`), which is useful for logging an experiment;
- `__eq__`, so two configs with the same values compare as equal.

Without it, we would write and maintain an `__init__` with five parameters and five `self.x = x` lines, plus `__repr__` and `__eq__`, and update all of them each time a setting is added.

`field(default_factory=lambda: list(DEFAULT_COLUMNS))` also avoids the mutable default trap: each `PipelineConfig` gets its own fresh copy of the column list, so changing `config.columns` in one experiment cannot change it in all the others.

## Why split responsibilities across `data.py`, `features.py` and `evaluation.py`

- **Each file has one reason to change.** Changing how missing values are filled only touches `data.py`; adding a feature only touches `features.py`; adding a metric only touches `evaluation.py`. Changes stay small and do not break unrelated code.
- **Easy to find and fix code.** `workflows.py` calls `data.load_datasets`, `features.add_temporal_features`, `evaluation.evaluate_manual_split`: the module name says which file to open.
- **Testable in isolation.** Each module has its own test file (`test_data.py`, `test_features.py`, `test_evaluation.py`). When a test fails, the bug is narrowed down to one module and one function, instead of somewhere in a long script.
- **Reusable building blocks.** `run_baseline` only assembles the pieces. Session 3 can reuse the same data and feature functions with another model or another evaluation (`GroupKFold`) without rewriting the pipeline.
- **Incremental, reviewable history.** Each module can be implemented, tested and committed separately, so the Git history shows the transformation one reviewable step at a time.
