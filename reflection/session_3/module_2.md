# Module 2 — Advanced Cleaning

## Question 1 — Why drop the high-missing columns before the per-city fill?

`fill_missing_by_city` only uses the values of the same city. If a city has no value at all for a column, there is nothing to copy, and the column stays empty for this city. This is what happens with Bujumbura: `uvaerosollayerheight_aerosol_height` is missing 100 % of the time there. After the fill, its 123 rows still have a NaN, and `LinearRegression` crashes with `Input X contains NaN` when we test on Bujumbura.

If we drop the column first, the fill only works on columns that have enough data, and nothing is left missing.

There is a second reason: the fill hides the problem. After filling, an almost empty column looks complete, but its values are just copies of a few real measures. In Kampala and Nairobi, aerosol height was 93–97 % missing, so after the fill almost all its values are fake. If we fill first, we cannot see anymore that the column was almost empty. So the decision "drop or fill" must be taken on the raw data, before the fill.

## Question 2 — What would `columns_above_missing_threshold` report on already-filled data?

Almost nothing. After the fill, every column is complete in every city that has at least one value, so the missing ratio is 0 %. The only NaN left are the 123 Bujumbura rows of aerosol height, which is 1.5 % of the 8071 rows. This is far below 0.7, so the function returns an empty list.

So on filled data, the function would say "nothing to drop", even though aerosol height was 94.7 % missing in the raw data and is still completely empty for Bujumbura. The check only makes sense on the raw data.

## Question 3 — Why 0.7, and what would 0.5 change?

On the raw data of the four cities, the missing ratios are:

| Column | Missing (%) |
|---|---|
| aerosol height | 94.7 |
| NO2 | 61.5 |
| SO2 | 60.9 |
| HCHO | 48.5 |
| CO | 45.0 |
| cloud fraction | 38.1 |
| ozone | 1.4 |
| aerosol index | 0.1 |

With 0.7, only aerosol height is dropped. It is the only column that is really almost empty, and it was not useful anyway (not significant in Module 1). All the others still have at least about 40 % of real values, which is enough to fill the gaps.

With 0.5, we also drop NO2 and SO2. SO2 is not a big loss (correlation about 0 in Module 1), but NO2 is the second most correlated variable with PM2.5 (r = 0.40). So a lower threshold removes useful information.

I tested both thresholds with `run_advanced`, training on Kampala:

| Test city | RMSE (0.7) | R² (0.7) | RMSE (0.5) | R² (0.5) |
|---|---|---|---|---|
| Bujumbura | 19.18 | 0.258 | 18.81 | 0.286 |
| Nairobi | 25.11 | −0.011 | 25.37 | −0.032 |
| Lagos | 52.19 | 0.024 | 52.90 | −0.003 |

The results are mixed: 0.5 is a bit better on Bujumbura, but a bit worse on Nairobi and Lagos. The differences are small, and Bujumbura only has 123 rows, so I would not conclude that 0.5 is better. 0.7 is a safer choice: it only drops the column that clearly cannot be filled, and keeps NO2. The threshold is a choice, not a fixed rule. The right way to choose it would be to compare the results on every city with a proper evaluation (Module 3, `GroupKFold`).
