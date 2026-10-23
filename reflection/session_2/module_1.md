# Module 1 — Understand the Air Quality Problem

## Question 1 — What do we know, and what is missing?

We know the goal: predict PM2.5 on the ground using satellite data from Sentinel-5P. We work on two cities, Kampala and Nairobi, and we want to know if a model trained on one city also works on the other. We also know the list of variables: city, date, hour, the coordinates of the station, the target `pm2_5`, and 8 satellite measurements (SO2, CO, NO2, HCHO, aerosol index, O3, aerosol height, cloud fraction).

A lot of things are missing:
- How many stations there are in each city, and where they are (near a road, in a residential area, near factories...).
- The time period of the data, and if it is the same for both cities.
- How PM2.5 is measured on the ground (professional sensor or cheap sensor) and if it is an hourly value or a daily average.
- How a satellite pixel is matched with a station, and how the time of the satellite pass is matched with the time of the ground measurement.
- The units of the satellite columns, and why some values are missing (clouds, no satellite pass...).
- Weather data like wind, rain or humidity. These have a big effect on PM2.5, but they are not in the dataset.

## Question 2 — Who would use this model, and why should they trust it?

The model could be used by:
- city or health agencies, to warn people on very polluted days or to decide where to act first;
- NGOs or national agencies, to estimate pollution in places without any sensor, and to choose where to put new sensors;
- researchers, to study the effect of pollution on health over large areas.

To trust it, they would need to see that:
- it was tested on places it has never seen (another city or other stations), because the goal is to predict where there is no sensor;
- the error is given in µg/m³ and compared with health limits, like the WHO guidelines;
- it works well on very polluted days, because those are the days when decisions are made;
- its limits are written clearly, for example that it cannot predict on cloudy days when the satellite has no data.

## Question 3 — Which variables are useful?

I expect these variables to be useful, because they are real physical measurements:
- CO and NO2: they come from combustion (traffic, burning), like a big part of PM2.5.
- The aerosol index: it measures particles like smoke and dust in the air.
- HCHO: it is linked to burning biomass.
- SO2: linked to industry, but the signal is often weak in cities.
- O3, cloud fraction and aerosol height: they give information about the atmosphere and about the quality of the satellite measure.
- The date, if we turn it into month or day of the week, because pollution changes with seasons and with the week.

These variables look more like identifiers:
- `city`: it is just a label. It is useless as a feature if we test on a city the model has never seen.
- `site_latitude` and `site_longitude`: they mostly tell which station it is. Inside one city they change very little, so the model can use them like a station ID, and then fail in another city.
- the raw `date`: it tells when the measure was taken, but the model cannot learn a pattern from it directly.

## Question 4 — What can happen if we use Kampala to train and then test on Nairobi?

1. The sources of pollution are not the same in the two cities (traffic, industry, cooking, burning). So the link between the satellite data and PM2.5 learned in Kampala may be wrong in Nairobi.
2. The geography and climate are different. Nairobi is higher than Kampala, and the rainy seasons and winds are not the same. The same satellite value can mean a different PM2.5 on the ground.
3. The coordinates of the two cities are completely different. If the model uses latitude and longitude, it will have to predict for values it has never seen, and the predictions can be absurd.
4. The data is not the same: not the same number of stations, not the same period, not the same amount of missing values. The model could learn things that are only true for Kampala.
5. If the ground sensors are not the same type in Nairobi, the target itself is not measured the same way.

## Question 5 — Type, scale and role of each variable

| Variable | Expected type or scale | Possible analytical role |
|----------|------------------------|--------------------------|
| city | Categorical (nominal) | Group: used to split train and test by city, not used as a feature |
| date | Date (interval scale) | Used to create month and day of week, and to sort the data in time |
| hour | Number, cyclic (interval scale) | Possible feature for the daily cycle; also the time of the satellite pass |
| site_latitude | Continuous number (interval scale) | Identifies the station; risky as a feature between cities |
| site_longitude | Continuous number (interval scale) | Identifies the station; risky as a feature between cities |
| pm2_5 | Continuous number, ratio scale (µg/m³, ≥ 0) | Target |
| sulphurdioxide_so2_column_number_density | Continuous number, ratio scale (mol/m²) | Possible feature (industry, fuel burning) |
| carbonmonoxide_co_column_number_density | Continuous number, ratio scale (mol/m²) | Possible feature (combustion) |
| nitrogendioxide_no2_column_number_density | Continuous number, ratio scale (mol/m²) | Possible feature (traffic, combustion) |
| formaldehyde_tropospheric_hcho_column_number_density | Continuous number, ratio scale (mol/m²) | Possible feature (biomass burning) |
| uvaerosolindex_absorbing_aerosol_index | Continuous number, index without unit (can be negative) | Possible feature (smoke, dust) |
| ozone_o3_column_number_density | Continuous number, ratio scale (mol/m²) | Possible feature / information about the atmosphere |
| uvaerosollayerheight_aerosol_height | Continuous number, ratio scale (m) | Possible feature, but almost always missing |
| cloud_cloud_fraction | Continuous number, between 0 and 1 | Context: quality of the satellite measure, weather |

## Notes from the discovery notebook

- **Data available:** Kampala has 30 stations and 5,596 rows (January 2023 to February 2024). Nairobi has 12 stations and 1,500 rows (May 2023 to January 2024). The two periods only partly overlap. All measures are taken between 10:00 and 12:00, when the satellite passes, so `hour` gives almost no information.
- **PM2.5 values:** most values are low, with a few very high ones. Kampala has a slightly higher median (about 18 vs 15 µg/m³). Nairobi has a few extreme values, up to about 456 µg/m³.
- **Over time:** there are peaks in Kampala in January–February 2023 and February 2024 (maybe the dry season), and in Nairobi in November 2023.
- **Missing values:** aerosol height is almost empty (93 to 97 % missing). NO2, SO2, HCHO, CO and cloud fraction have between 35 and 68 % missing. Ozone and aerosol index are almost complete. Both cities look the same, so the problem probably comes from the satellite, not from one city.
- **Correlations with PM2.5:** CO and NO2 are around +0.31, HCHO +0.17, ozone −0.18, the others close to 0. No variable is strongly linked to PM2.5, so a linear model will probably not predict very well.
