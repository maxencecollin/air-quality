# Module 6 — Experiment Tracking

I ran `scripts/run_tracked_tuning.py`. It rebuilds the Module 4 data (same 8 RFE columns), reruns the Module 5 grid search, and logs each of the 4 combinations as one MLflow run in the `air_quality` experiment. Each run has 2 params (`max_depth`, `learning_rate`) and 3 metrics (`rmse`, `mae`, `r2`).

The Runs table in `mlflow ui`, sorted by `rmse`:

| Run | max_depth | learning_rate | rmse | mae | r2 |
|---|---|---|---|---|---|
| xgb_depth3_lr0.05 | 3 | 0.05 | 27.57 | 14.24 | 0.085 |
| xgb_depth3_lr0.2 | 3 | 0.2 | 28.79 | 15.89 | −0.074 |
| xgb_depth5_lr0.05 | 5 | 0.05 | 28.89 | 14.77 | −0.092 |
| xgb_depth5_lr0.2 | 5 | 0.2 | 31.07 | 17.28 | −0.492 |

## Which combination won, and does it match Module 5?

The winner is `max_depth=3`, `learning_rate=0.05`, with an RMSE of 27.57. This is exactly the same as in Module 5: same best combination, same numbers for all four runs. This is normal, because the data, the 8 columns, the folds and the `random_state` are the same. MLflow does not change the results, it only stores them.

## Would I have found it as quickly in Module 5's printed results?

With only 4 runs, yes. In Module 5 the notebook already showed the `cv_results` table sorted by `rmse`, and 4 lines are easy to read.

But MLflow gives more than a quick answer. In Module 5, the results only exist in the notebook output: if I rerun the cell, the old results are gone. In MLflow, every run is saved with its params and metrics, with a date. I can sort by any column, filter (`metrics.rmse < 28`), and compare runs made on different days, or with different scripts. In the notebook, I would have to remember or copy the old numbers by hand.

## At how many runs does "re-run and read the terminal" stop being practical?

I think around 10 to 20 runs. Up to about 10, a printed table fits on one screen and I can still compare the lines by eye. After that, I have to scroll, and I cannot easily see which params go with which result.

The real problem is not only the number of runs, it is when they are made at different times or with different settings. Even 5 runs made on 3 different days, with some changes in the code between them, are already hard to follow in the terminal, because the old output is lost. As soon as I want to compare today's run with last week's run, I need a tool that keeps a record.

A bigger grid would arrive very fast: 3 values for 4 hyperparameters is already 81 runs. Without tracking, nobody can read that.
