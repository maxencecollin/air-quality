# Module 1 — Understand the Air Quality Problem

## Question 1 — What the problem statement gives, and what is missing

**Available:**
- The goal: predict ground-level PM2.5 concentration from Sentinel-5P satellite measurements.
- The scope: two cities, Kampala and Nairobi, with the explicit question of whether a model transfers from one city to the other.
- The variables: city, date, hour, site coordinates, the target `pm2_5`, and eight satellite-derived measurements (SO2, CO, NO2, HCHO, UV aerosol index, O3, aerosol layer height, cloud fraction).

**Missing:**
- How many monitoring stations there are per city, and where they sit (city centre, roadside, residential, industrial).
- The time period covered, and whether it is the same for both cities.
- How PM2.5 was measured on the ground: reference-grade monitors or low-cost sensors, calibration, and whether `pm2_5` is an hourly reading or an average over a longer window.
- How satellite pixels were matched to stations (spatial resolution, distance tolerance) and to time (overpass time vs. ground measurement time).
- Units of the satellite columns and the meaning of a missing value (cloud cover, failed retrieval, no overpass).
- Weather data (wind, rain, humidity, boundary layer height), which strongly drives PM2.5 but is absent from the variable list.

## Question 2 — Who would use the model, and what makes it trustworthy

**Users and decisions:**
- City environmental and public health agencies: issue pollution alerts, target traffic or burning restrictions, prioritise districts for interventions.
- National agencies and NGOs: estimate exposure in areas with no ground sensor, and decide where to install the next stations.
- Researchers: study long-term exposure and its health effects at a scale ground networks cannot cover.

**What would make it trustworthy:**
- Validation on places it has never seen (another city, or held-out stations), not only on a random split, because the whole point is to predict where there are no sensors.
- Errors reported in µg/m³ and compared with health thresholds (e.g. WHO guidelines), with a clear statement of uncertainty.
- Good behaviour on high-pollution days, since those are the ones that trigger decisions.
- Transparency about which inputs drive predictions, and stable performance over time and seasons.
- Honest documentation of the limits: cloudy days with no satellite data, cities or seasons absent from training.

## Question 3 — Informative predictors vs. identifiers

**Likely informative (physical measurements):**
- `carbonmonoxide_co_column_number_density` and `nitrogendioxide_no2_column_number_density`: combustion tracers (traffic, biomass burning), which share sources with PM2.5.
- `uvaerosolindex_absorbing_aerosol_index`: directly related to absorbing aerosols (smoke, dust) in the atmosphere.
- `formaldehyde_tropospheric_hcho_column_number_density`: linked to biomass burning and secondary aerosol formation.
- `sulphurdioxide_so2_column_number_density`: industrial and fuel combustion, but the signal is usually weak over cities.
- `ozone_o3_column_number_density`, `cloud_cloud_fraction`, `uvaerosollayerheight_aerosol_height`: indirect information on atmospheric conditions and on the quality of the satellite retrieval.
- `date` and `hour`, once turned into month or day of week: seasonal and weekly cycles of pollution.

**Look more like identifiers:**
- `city`: a label for the group, not a physical measurement. Using it as a feature makes no sense when testing on a city the model has never seen.
- `site_latitude` / `site_longitude`: they mostly identify a station. Within one city they vary over a tiny area, so a model can latch onto them as station IDs and fail completely elsewhere.
- `date` as a raw timestamp: it identifies when a reading was taken, but does not by itself carry a pattern a model can reuse.

## Question 4 — Risks of training on Kampala and applying to Nairobi

1. **Different pollution sources and levels:** the mix of traffic, industry, cooking fuels and biomass burning differs between the cities, so the relationship between satellite columns and ground PM2.5 learned in Kampala may not hold in Nairobi.
2. **Different geography and climate:** Nairobi is at a much higher altitude (~1,700 m vs. ~1,200 m), with a different rainy season pattern and wind regime. The same satellite column can correspond to a different ground concentration.
3. **Extrapolation on coordinates:** Kampala and Nairobi occupy disjoint latitude/longitude ranges. A model using raw coordinates would extrapolate far outside what it has seen and can produce absurd predictions.
4. **Different data coverage:** the two cities do not have the same number of stations, the same time period, or the same missing-value rates. The model could learn patterns tied to Kampala's specific periods and stations.
5. **Different measurement setup:** if ground sensors are of a different type or calibration in Nairobi, the target itself is not measured the same way.

## Question 5 — Type, scale and role of every variable

| Variable | Expected type or scale | Possible analytical role |
|----------|------------------------|--------------------------|
| city | Categorical, nominal | Group identifier: used to split train/test by city, not as a feature |
| date | Datetime (interval scale) | Source of temporal features (month, day of week); ordering for time-aware cleaning |
| hour | Discrete numeric, cyclic (interval scale) | Potential feature for daily cycle; also reflects satellite overpass time |
| site_latitude | Continuous numeric (interval scale) | Location identifier; risky as a raw feature (extrapolation across cities) |
| site_longitude | Continuous numeric (interval scale) | Location identifier; risky as a raw feature (extrapolation across cities) |
| pm2_5 | Continuous numeric, ratio scale (µg/m³, ≥ 0) | Target variable |
| sulphurdioxide_so2_column_number_density | Continuous numeric, ratio scale (mol/m²) | Candidate predictor (industrial / fuel combustion) |
| carbonmonoxide_co_column_number_density | Continuous numeric, ratio scale (mol/m²) | Candidate predictor (combustion tracer) |
| nitrogendioxide_no2_column_number_density | Continuous numeric, ratio scale (mol/m²) | Candidate predictor (traffic / combustion tracer) |
| formaldehyde_tropospheric_hcho_column_number_density | Continuous numeric, ratio scale (mol/m²) | Candidate predictor (biomass burning, secondary aerosols) |
| uvaerosolindex_absorbing_aerosol_index | Continuous numeric, dimensionless index (interval scale, can be negative) | Candidate predictor (smoke, dust) |
| ozone_o3_column_number_density | Continuous numeric, ratio scale (mol/m²) | Candidate predictor / atmospheric context |
| uvaerosollayerheight_aerosol_height | Continuous numeric, ratio scale (m) | Candidate predictor, but mostly missing |
| cloud_cloud_fraction | Continuous numeric, proportion in [0, 1] | Context variable: retrieval quality, weather proxy |

## Notes from the discovery notebook

Observations to reuse when interpreting the model in the next activity:

- **Coverage:** Kampala has 30 stations and 5,596 readings (Jan 2023 – Feb 2024); Nairobi has 12 stations and 1,500 readings (May 2023 – Jan 2024). The periods only partly overlap, with gaps at the end of 2023. Readings are only taken between 10:00 and 12:00, which matches the satellite overpass, so `hour` carries almost no daily-cycle information.
- **Distribution:** PM2.5 is right-skewed in both cities. Kampala has a slightly higher median (~18 vs. ~15 µg/m³) and a tighter spread; Nairobi has a few isolated extreme values (up to ~456 µg/m³).
- **Time:** visible peaks in Kampala in Jan–Feb 2023 and Feb 2024 (dry season?), and in Nairobi in Nov 2023. Some Nairobi days have very wide confidence intervals.
- **Missing values:** aerosol layer height is almost empty (93–97 % missing); NO2, SO2, HCHO, CO and cloud fraction miss 35–68 %; ozone and aerosol index are nearly complete. Profiles are similar in both cities, pointing to a satellite retrieval limitation rather than a city-specific sensor problem.
- **Correlations with PM2.5:** CO and NO2 ≈ +0.31, HCHO ≈ +0.17, ozone ≈ −0.18, the rest ≈ 0. No strong linear relationship: a linear model is likely to have limited predictive power.
