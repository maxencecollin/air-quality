# Module 2 — Build a First Pipeline

## Question 1 — Training on Nairobi and testing on Kampala

Baseline `LinearRegression` (features: `hour`, the 8 satellite columns, `month`, `dayofweek`; 1200 rows per city, `random_state=42`):

| Train → Test      | RMSE  | MAE   | R²     |
|-------------------|-------|-------|--------|
| Kampala → Nairobi | 24.59 | 10.03 | -0.022 |
| Nairobi → Kampala | 15.17 | 11.02 | -0.158 |

**What the difference tells us:**
- The RMSE depends heavily on which city is held out (24.6 vs. 15.2), while the MAE stays around 10–11 µg/m³ in both directions. The gap in RMSE mostly comes from Nairobi's few extreme values (up to ~456 µg/m³), which RMSE squares and therefore penalises heavily when Nairobi is the test city.
- R² is negative in both directions: the model does worse than simply predicting the test city's mean PM2.5. What it learned in one city does not transfer to the other.
- A single train/test split gives an unstable picture of generalisation: change the held-out city and the conclusion changes. A reliable estimate needs several held-out groups, which is what `GroupKFold` will provide in Session 3.
- Adding the raw coordinates makes it far worse (RMSE ≈ 333 and ≈ 194, R² ≈ -186 and -188): the model fits huge coefficients on a tiny geographic area and extrapolates them to a city it has never seen.

**Would I deploy either direction?** No. An average error of ~10 µg/m³ when the median PM2.5 is ~15–18 µg/m³ is too large, and a negative R² means a constant prediction would do better. The large RMSE also suggests the model is far off on the high-pollution days, which are the ones that would trigger a decision. Before deploying, it would at least need to beat a simple mean baseline on several held-out cities or stations.

## Question 2 — CRISP-DM phases covered so far

| CRISP-DM phase         | Where it happened |
|------------------------|-------------------|
| Business Understanding | Module 1 reflection: what the problem statement gives and lacks, who would use the model and why, expected predictors vs. identifiers, risks of transferring from one city to another |
| Data Understanding     | Module 1 discovery notebook: PM2.5 distributions, daily trends, missing values per city, correlations with satellite columns |
| Data Preparation       | Module 2 pipeline, steps 1–4: scope and sampling, per-city forward/backward fill, split by city, `month`/`dayofweek` features |
| Modeling               | Module 2 pipeline, step 5: `LinearRegression` fit |
| Evaluation             | Module 2 pipeline, step 5 and going further: RMSE/MAE/R², reversed split, coordinate experiment |
| Deployment             | Not reached |

Building and evaluating this baseline pipeline belongs mainly to the **Modeling** and **Evaluation** phases, with steps 1–4 being **Data Preparation**. The poor evaluation results send us back to earlier phases, as CRISP-DM is iterative: rethinking the features (Data Preparation), and possibly the problem framing itself (Business Understanding), before trying more models.
