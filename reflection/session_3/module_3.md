# Module 3 — Robust Evaluation

I used `GroupKFold` with one fold per city: each city is the test set once, and the `LinearRegression` is trained on the three other cities. The data is the cleaned 4-city dataset from Module 2 (aerosol height dropped, the rest filled per city).

| City held out | RMSE | MAE | R² |
|---|---|---|---|
| Kampala | 13.40 | 9.67 | 0.127 |
| Nairobi | 25.19 | 10.15 | −0.018 |
| Lagos | 52.01 | 22.87 | 0.030 |
| Bujumbura | 19.74 | 12.61 | 0.214 |
| **Mean ± std** | **27.58 ± 14.71** | **13.82 ± 5.34** | **0.088 ± 0.089** |

## Question 1 — Which city has the highest RMSE when held out?

Lagos has the highest RMSE = 52.0, almost 4 times Kampala (13.4) and twice Nairobi (25.2). The MAE is also the highest (22.9).

Lagos is the most polluted city in the dataset, and it has many very high values: its mean (46) is much higher than its median (33). I checked the predictions when Lagos is held out: the median prediction (34) is close to the real median, but the mean prediction (36) is far below the real mean (46). So the model is not wrong on typical days, it misses the very polluted days. These big errors make the RMSE increase, because RMSE squares the errors. The model is trained mostly on Kampala and Nairobi, where such high values are rare, so it never learned to predict them.

In Session 2 we never saw this problem, because we only used Kampala and Nairobi.

## Question 2 — Does the mean RMSE match one of Session 2's numbers?

No,the mean RMSE across the four folds is 27.6. In Session 2 we had 24.6 (Kampala → Nairobi) and 15.2 (Nairobi → Kampala). The mean is higher than both, mostly because of Lagos.

Some single folds are close to Session 2: when Nairobi is held out, the RMSE is 25.2, very close to the 24.6 of Session 2. When Kampala is held out, it is 13.4, close to 15.2. But the setup is not exactly the same: Session 2 used 1200 rows per city and trained on only one city, here we use all rows and train on three cities.

So each Session 2 number described one case only. Neither of them was a good estimate of how the model works in general.

## Question 3 — What does a large std across folds tell us?

The std of the RMSE is 14.7, for a mean of 27.6. This means the error changes a lot depending on which city is used for the test: from 13 to 52.

So one train/test pair, like in Session 2, gives a number that depends mostly on the city we chose. If we had picked Kampala as the test city, we would have said "RMSE about 13, not bad". If we had picked Lagos, we would have said "RMSE about 52, very bad". Both would be true for that city, and both would be misleading for a new city.

A large std means we cannot trust a single number. We have to look at the result for each city and give the mean together with the std. Here, the honest answer is: "on a city the model has never seen, the RMSE is about 28, but it can go from 13 to 52 depending on the city".
