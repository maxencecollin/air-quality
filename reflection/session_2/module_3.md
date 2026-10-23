# Module 3 — Transfer to Python

## Why a notebook alone is not enough

1. **The result depends on the order of the cells.** In a notebook, variables stay in memory and depend on which cells were run before. In `02_pipeline.ipynb`, `train_df` only has `month` and `dayofweek` if the step 4 cell was run after step 3. The "Going further" cell also uses `feature_cols` from step 5 without saying it. A function in `src/air_quality/` gets everything it needs as parameters and returns a result, so it always gives the same result.
2. **No more copy-paste.** In the notebook, I wrote the fit/predict/metrics code in step 5, then I had to write it again in an `evaluate` function for the reversed split. With a module, `evaluation.evaluate_manual_split` is written once and can be used from a notebook, a script or Session 3.
3. **Automatic tests.** To check a notebook, I have to run it again and look at the output. With functions in `src/`, `pytest` checks each function by itself in a few seconds. For example, it checks that `fill_missing_by_city` never fills one city with the values of another city. If I break something, I see it right away.
4. **It runs without Jupyter.** `scripts/run_pipeline.py --train-city Nairobi --test-city Kampala` runs the whole pipeline from the terminal. No need to open a notebook or click on cells. Someone else, or an automatic job, can run it the same way.
5. **Git diffs are readable.** A `.ipynb` file is JSON with images and run numbers inside, so a small change gives a big diff that is hard to read. With a `.py` file, each commit shows exactly which function changed.

## What is a `dataclass`, and what does it save for `PipelineConfig`?

A `dataclass` is a class with the `@dataclass` decorator. We only write the attributes with their type and default value, and Python writes the usual methods for us. For `PipelineConfig`, it creates:
- `__init__`, which takes `train_city`, `test_city`, `columns`, `max_rows_per_city` and `random_state` as arguments and stores them in `self`;
- `__repr__`, so printing a config shows all its values, for example `PipelineConfig(train_city='Kampala', ...)`;
- `__eq__`, so two configs with the same values are equal.

Without it, I would have to write an `__init__` with 5 parameters and 5 lines `self.x = x`, plus `__repr__` and `__eq__`, and change all of them every time I add a setting.

`field(default_factory=lambda: list(DEFAULT_COLUMNS))` also avoids a classic bug: each `PipelineConfig` gets its own copy of the column list. If I change `config.columns` in one experiment, it does not change the list in the other configs.

## Why split the code into `data.py`, `features.py` and `evaluation.py`?

- **Each file has one job.** If I change how missing values are filled, I only touch `data.py`. If I add a feature, only `features.py`. If I add a metric, only `evaluation.py`. Changes stay small and do not break the rest.
- **It is easy to find the code.** In `workflows.py`, the calls look like `data.load_datasets`, `features.add_temporal_features` or `evaluation.evaluate_manual_split`. The module name tells me which file to open.
- **Each part can be tested alone.** Each module has its own test file. When a test fails, I know which module and which function to look at.
- **The functions can be reused.** `run_baseline` only puts the pieces together. In Session 3, I can reuse the same functions with another model or another evaluation, like `GroupKFold`, without rewriting everything.
- **The Git history is clear.** Each module was written, tested and committed separately, so the history shows the work step by step.
