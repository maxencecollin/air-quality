# Module 4 — Feature Selection

I used all 70 satellite columns. After the Module 2 cleaning (7 `uvaerosollayerheight_*` columns dropped because more than 70 % missing), 66 features were left. I compared three feature sets with `GroupKFold` (one fold per city) and a `LinearRegression`:

| Feature set | Kampala | Nairobi | Lagos | Bujumbura | Mean RMSE | Mean R² |
|---|---|---|---|---|---|---|
| All 66 features | 15882.7 | 25.2 | 51.4 | 20.8 | 3995.03 | −306447 |
| SelectKBest (8) | 35.1 | 25.2 | 51.1 | 19.9 | 32.84 | −1.187 |
| RFE (8) | 13.9 | 25.2 | 51.1 | 20.3 | 27.63 | 0.068 |
| Module 3 (8 hand-picked columns) | 13.4 | 25.2 | 52.0 | 19.7 | 27.58 | 0.088 |

(RMSE per held-out city, in µg/m³.)

## Why does RFE come close to the hand-picked columns, while SelectKBest does worse?

**RFE** gets a mean RMSE of 27.63, almost the same as the 27.58 of Module 3 with the columns chosen by hand. RFE fits the model with all the remaining features at each step, and removes the one that helps the least. If two columns say the same thing, the second one adds nothing once the first is in the model, so it is removed. In the end, RFE kept only pollutant measurements: CO, NO2, SO2 and HCHO. These are almost the same kind of columns that a human picked in Session 2, so it is normal that the score is close. The algorithm found it alone, without any domain knowledge.

RFE is not perfect: it still kept 4 versions of NO2 (total, tropospheric, stratospheric, slant), which are strongly correlated with each other (about 0.97 for two of them). But this did not hurt the result much.

**SelectKBest** also keeps 8 columns, but 4 of them are `solar_azimuth_angle` columns from different satellite products (SO2, CO, aerosol index, ozone). These 4 columns are correlated at 0.98–0.99 with each other: they are the same information (the position of the sun, so roughly the time of the satellite pass) repeated four times. SelectKBest scores each column alone against PM2.5, so each angle looks useful, and it keeps all of them. It cannot see that they are duplicates. So half of its budget is wasted, and the model has redundant columns again.

The table shows where it hurts: on Kampala, SelectKBest gets an RMSE of 35.1 and R² = −4.99, against 13.9 for RFE. On the other cities, the three methods are almost the same. So the bad mean of SelectKBest comes mostly from one city.

## When is a univariate method enough?

A univariate method like SelectKBest is fine when the features are not strongly correlated with each other. In that case, the columns that are the most linked to the target are also different pieces of information, and taking the top k works well. It is also fast, which is useful with a very large number of columns, for example as a first filter before a slower method.

But when many columns are near-duplicates, which is the case here (dozens of pairs above 0.9), a univariate method will pick the same information several times. Then we need a method that looks at the features together, like RFE, or we have to remove the duplicates first (for example by dropping one column of each pair with a correlation above 0.9).

## Why the all-features model should not be trusted

With all 66 features, the largest coefficient is about **−358,825** (on `nitrogendioxide_stratospheric_no2_column_number_density`), while PM2.5 is never above 456 µg/m³. Coefficients this big are a sign of multicollinearity: the model cannot decide how to share the effect between columns that say the same thing.

Out of sample, it explodes: when Kampala is held out, the RMSE is **15,882.7 µg/m³** and R² is about **−1.2 million**. The mean RMSE over the four cities is 3,995. A model that can be wrong by thousands of µg/m³ on a whole city cannot be used, even if it looks fine on the other cities.

## A limit of this comparison

The features were selected on the data of all four cities, and then evaluated with `GroupKFold` on the same data. So the held-out city had a small influence on which columns were chosen. This is a small leak of information, and it makes the scores a bit too optimistic. To be fully correct, the selection should be done inside each fold, only on the training cities (for example with a scikit-learn `Pipeline`).
