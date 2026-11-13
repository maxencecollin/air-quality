# Module 5 — Hyperparameter Tuning

I used the same 8 columns chosen by RFE in Module 4, and the same evaluation: `GroupKFold` with one fold per city. I compared four models:

| Model | Kampala | Nairobi | Lagos | Bujumbura | Mean RMSE | Mean R² |
|---|---|---|---|---|---|---|
| XGBoost, untuned (defaults) | 29.5 | 26.0 | 52.1 | 19.9 | 31.88 | −0.773 |
| XGBoost, worst grid point (`max_depth=5`, `learning_rate=0.2`) | 24.9 | 26.3 | 52.6 | 20.4 | 31.07 | −0.492 |
| XGBoost, best grid point (`max_depth=3`, `learning_rate=0.05`) | 13.7 | 24.9 | 51.8 | 19.8 | **27.57** | 0.085 |
| LinearRegression (Module 4) | 13.9 | 25.2 | 51.1 | 20.3 | 27.63 | 0.068 |

(RMSE per held-out city, in µg/m³.)

The two other grid points were in between: 28.79 (`max_depth=3`, `learning_rate=0.2`) and 28.89 (`max_depth=5`, `learning_rate=0.05`).

## Was it worth introducing a more complex model?

Not really. The tuned XGBoost is the best model, but only by 0.06 µg/m³ (27.57 against 27.63). This is very small compared to the difference between cities (from 14 to 52). On Lagos, the linear model is even a little better. So with these 8 columns, XGBoost does not find much more than a straight line.

And the untuned XGBoost is clearly worse than the linear model (31.88). So a complex model is only useful if we take the time to tune it. Here, after tuning, we just come back to the level of the simple model. The linear model is easier to explain and faster, so I would keep it, unless we add new information (new columns, more data) that XGBoost could use better.

I think the problem is not the model but the data: with only satellite columns, the model does not have enough information to predict PM2.5 in a new city. Lagos stays at about 52 for every model.

## What does the gap between the best and worst combination show?

With the same model and the same 8 columns, only changing two settings moves the RMSE from 27.57 to 31.07. Almost all of this gap comes from Kampala: 13.7 with the best settings, 24.9 with the worst. So a bad choice of hyperparameters can cost more than the choice between XGBoost and a linear model (0.06).

The best settings are the most careful ones: small trees (`max_depth=3`) and slow learning (`learning_rate=0.05`). The untuned model uses the defaults (`max_depth=6`, `learning_rate=0.3`), which are more aggressive. On all the data, it has an RMSE of 13.5 on the rows it was trained on, but 31.9 on new cities: it learns the training cities by heart (overfitting). The best model has 21.4 on its training rows and 27.6 on new cities: it learns less detail, but what it learns works better on a city it has never seen.

Kampala is the fold where this matters most. Kampala has 5,596 of the 8,071 rows, so when it is held out, the model is trained on only about 2,500 rows from the three other cities. With few data, a flexible model overfits more easily.

So tuning is not a detail: it decides whether a model is good or bad, whatever model we choose. And we must look at all the combinations, not only the best one, to see how much the settings matter.

## A limit

The grid is very small (4 combinations, 2 hyperparameters). I tuned on the same folds that I use to report the score, so the 27.57 is a bit optimistic. To be fully correct, we would need a nested cross-validation (tuning inside each fold). The 8 columns were also chosen by RFE on all four cities, like in Module 4.
