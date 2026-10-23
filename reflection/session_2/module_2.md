# Module 2 — Build a First Pipeline

## Question 1 — Train on Nairobi, test on Kampala

I used a `LinearRegression` with these features: `hour`, the 8 satellite columns, `month` and `dayofweek`. Each city has 1200 rows (`random_state=42`).

| Train → Test      | RMSE  | MAE   | R²     |
|-------------------|-------|-------|--------|
| Kampala → Nairobi | 24.59 | 10.03 | -0.022 |
| Nairobi → Kampala | 15.17 | 11.02 | -0.158 |

The RMSE changes a lot depending on which city is used for the test (24.6 vs 15.2). The MAE stays almost the same (around 10–11 µg/m³). The difference comes from the few very high values in Nairobi: RMSE squares the errors, so a few big errors make it go up a lot when Nairobi is the test city.

The R² is negative in both cases. This means the model is worse than just predicting the average PM2.5 of the test city. What it learns in one city does not work in the other one.

So one train/test split is not enough to know if a model generalizes: if we change the test city, the conclusion changes. We need to test on several cities, one after the other. This is what `GroupKFold` does in Session 3.

I also tried adding the latitude and longitude. The results become much worse (RMSE of about 333 and 194, R² of about −186). The model learns very big coefficients on a very small area, and then applies them to a city far away.

**Would I use this model for real?** No. The average error is about 10 µg/m³, when the median PM2.5 is only about 15–18 µg/m³. And with a negative R², just predicting the average would be better. The high RMSE also suggests that the model makes big mistakes on very polluted days, and these are the days that matter for decisions.

## Question 2 — Which CRISP-DM phases have we done?

| CRISP-DM phase         | What we did |
|------------------------|-------------|
| Business Understanding | Module 1 reflection: what the problem gives and what is missing, who would use the model, which variables look useful, risks between cities |
| Data Understanding     | Module 1 notebook: PM2.5 distribution, daily trends, missing values, correlations |
| Data Preparation       | Module 2 notebook, steps 1 to 4: sampling, filling missing values by city, split by city, month and day of week |
| Modeling               | Module 2 notebook, step 5: training the `LinearRegression` |
| Evaluation             | Module 2 notebook, step 5 and "going further": RMSE, MAE, R², reversed split, test with coordinates |
| Deployment             | Not done |

Building and testing this first pipeline is mostly **Modeling** and **Evaluation**. Steps 1 to 4 are **Data Preparation**. Since the results are bad, we have to go back to earlier phases. CRISP-DM works in loops: we should improve the features (Data Preparation), and maybe even rethink the problem (Business Understanding), before trying other models.
