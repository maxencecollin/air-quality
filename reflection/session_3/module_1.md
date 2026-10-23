# Module 1 — Rigorous Correlation Analysis

## Question 1 — How does `correlation_table` compare with Session 2?

In Session 2, with only Kampala and Nairobi, the quick heatmap gave: CO +0.31, NO2 +0.31, HCHO +0.17, ozone −0.18, aerosol index about 0, and the others close to 0.

With the four cities (Kampala, Nairobi, Lagos, Bujumbura), the Pearson correlations with PM2.5 are:

| Variable | n | Pearson r | Spearman rho | Significant (p ≤ 0.05)? |
|---|---|---|---|---|
| CO | 4441 | 0.42 | 0.52 | yes |
| NO2 | 3104 | 0.40 | 0.43 | yes |
| HCHO | 4156 | 0.20 | 0.28 | yes |
| Ozone | 7959 | −0.18 | −0.22 | yes |
| Aerosol index | 8066 | 0.17 | 0.13 | yes |
| Aerosol height | 427 | −0.04 | 0.03 | no |
| Cloud fraction | 4994 | −0.02 | 0.03 | no |
| SO2 | 3159 | 0.01 | −0.01 | no |

The order is almost the same: CO and NO2 are still at the top, and SO2, cloud fraction and aerosol height are still useless. But some things changed:
- CO and NO2 went up, from 0.31 to about 0.40. Adding Lagos and Bujumbura made the link stronger.
- The aerosol index changed the most: it was about 0 with two cities, and now it is 0.17 and significant.
- Spearman is higher than Pearson for CO (0.52 vs 0.42). So the link is not perfectly linear, or a few extreme PM2.5 values pull Pearson down.

Part of this change probably comes from the differences between cities, not from a real link inside each city. Lagos has a much higher median PM2.5 (about 33 µg/m³) than Kampala (18) and Nairobi (15). If Lagos also has higher CO, the global correlation goes up even if the link inside each city stays the same.

## Question 2 — Is `n` large enough to trust the top variable?

For CO, n = 4441 rows, and p is tiny (about 1e-192). So the correlation is clearly not due to chance. But a big n is not enough to trust it, because the rows are not spread evenly:

| City | Rows with CO and PM2.5 | Pearson r inside the city |
|---|---|---|
| Kampala | 2876 | 0.50 |
| Nairobi | 982 | 0.02 (not significant) |
| Lagos | 539 | 0.24 |
| Bujumbura | 44 | 0.81 |

- About 65 % of the rows come from Kampala, so the global result mostly describes Kampala.
- In Nairobi there is no link at all between CO and PM2.5 (r = 0.02). So "CO predicts PM2.5" is not true everywhere.
- Bujumbura has a very high r (0.81), but with only 44 rows. This is too small to be sure.

So n is large enough to say that the link exists in the whole dataset, but not to say it works the same in every city. The other thing to remember: r = 0.42 is a moderate link. The scatter plot shows a lot of spread, and the very high PM2.5 values (200 to 450) happen with low CO. CO alone cannot predict PM2.5 well.

## Question 3 — What would I investigate next?

- **Correlation city by city:** compute the table for each city separately, to see which links are real everywhere and which come only from differences between cities (like CO in Nairobi).
- **Variables linked to each other:** CO and NO2 are strongly correlated (0.62), and both are linked to the aerosol index (about 0.46). They partly carry the same information, so using all of them in a linear model could be a problem. This is for the Feature Selection module.
- **The extreme PM2.5 values:** check where and when they happen (which city, which station, which dates) and if they are real or sensor errors.
- **Non-linear links:** since Spearman is higher than Pearson, try a log transform of PM2.5 or CO, or a non-linear model.
- **Evaluation by city:** the results depend a lot on the city, so the model should be tested on each city one after the other. This is the Robust Evaluation module with `GroupKFold`.
