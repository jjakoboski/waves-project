# Preliminary New Hampshire surf-climate check

Calculated November 16, 2026. Uses complete calendar years 2021–2025 versus 2016–2020, with 2011–2020 as a longer baseline. Does not include 2026 or establish a precise five-year breakpoint.

## Sources

- NOAA NDBC annual standard meteorological archives: https://www.ndbc.noaa.gov/data/historical/stdmet/ ; files `{station}h{year}.txt.gz`, stations 44098 and 44007, 2011–2025.
- Jeffreys Ledge station metadata: https://cdip.ucsd.edu/a/stations/160p1/
- Parameter definitions: https://www.ndbc.noaa.gov/faq/measdes.shtml
- CPC NAO monthly index: https://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii
- Jamous & Marsooli (2023): https://www.mdpi.com/2077-1312/11/5/916
- NOAA wave generation: https://www.noaa.gov/jetstream/ocean/waves

## Method

Python standard library only. Run `python3 analyze.py`, `python3 directional.py`, and `python3 check.py` from this directory. Scripts read the downloaded archives in data/. No gap interpolation. Reject sentinel/out-of-range heights, periods and directions. Average records and threshold indicators within each UTC hour so reporting-frequency changes do not overweight observations. Compute monthly metrics; main comparison retains months with at least 80% hourly coverage. Average each calendar month across available years, then equally average the 12 calendar months. Thus percentages are seasonally standardized fractions of observed time, not raw counts of events or surf days. Height conditional on a direction is the standardized direction-weighted height divided by standardized direction occurrence.

Primary incoming-direction screening is 45–135 degrees true FROM (NE–SE), excluding waves whose dominant direction is from the western quadrants. Sensitivities: 0–135, 45–157.5 and 90–135 degrees. These are illustrative offshore exposure windows, NOT a validated coastwide transmission function. Cape Ann, local headlands, refraction and bathymetry affect actual beach arrival. Hs remains total significant wave height, even when peak direction and period pass a filter: this is NOT a partitioned incoming-swell height. Mixed seas can cause misclassification, and secondary incoming swell may be missed when outgoing wind waves dominate. Full directional spectra and nearshore wave modeling are required to remove these limitations.

## Results

Jeffreys Ledge, main NE–SE screening:

| Metric | 2016–2020 | 2021–2025 | Relative change |
|---|---:|---:|---:|
| Time dominant waves come from NE–SE, any height/period | 54.34% | 55.22% | +1.6% |
| Mean total Hs conditional on NE–SE dominant direction | 1.337 m | 1.206 m | -9.8% |
| Time Hs >=1 m, peak period >=8 s, NE–SE | 18.77% | 17.27% | -8.0% |
| Time Hs >=1.5 m, peak period >=8 s, NE–SE | 10.93% | 8.85% | -19.0% |
| Time Hs >=1 m, peak period >=10 s, NE–SE | 9.80% | 8.99% | -8.3% |

Stronger-condition indicator (Hs >=1.5 m, peak >=8 s, NE–SE): October–April 15.73% ->12.28% (-22.0%); May–September 4.19% ->4.04% (-3.6%). Broader NE–SSE screening gives -12.2% for Hs >=1 m/8 s and -22.4% for Hs >=1.5 m/8 s. Across tested direction sectors and 70/80/90% coverage cutoffs, stronger-condition declines remain approximately 18–24% versus 2016–2020.

Against 2011–2020, the primary NE–SE 1 m/8 s indicator declines 4.3%; the 1.5 m/8 s indicator declines 13.6%. Baseline selection matters. These are descriptive differences; no claim of a statistically significant climate trend is made.

All-direction context only: Jeffreys Ledge mean Hs 1.296 ->1.199 m (-7.5%); Portland 44007 0.986 ->0.956 m (-3.1%). These are not estimates of NH surf.

CPC NAO: October–April mean index +0.575 in 2016–2020 versus -0.022 in 2021–2025; full-year means +0.249 versus -0.068. Each uses all corresponding months from the named calendar years (not winter-year labeling). This does not establish causation or rule out NAO effects on individual episodes, but does contradict a simple explanation based on a more positive average NAO during the recent window.

## Interpretation

The record supports reduced time with stronger potentially incoming swell conditions, predominantly in the cold season, rather than fewer easterly directions overall. Changes in storm strength, location, duration and wave-generating fetch are plausible mechanisms; these were not directly attributed using storm-track or wind-field data. Five-year differences do not establish a permanent shift or an anthropogenic cause. Event arrival counts cannot be inferred from exceedance time alone: shorter events and fewer events both reduce exceedance time. Beach morphology and local winds were not measured here.

## Year-by-year follow-up: >3 m and >=8 seconds, NE–SE

See yearly_results.csv, yearly_analysis.txt and yearly.py. Annual observed percentages weight monthly threshold fractions by observed valid hours (coverage times calendar hours). Coverage uses all calendar hours, including entirely absent months: April 2016 and April 2022 have no valid records. These annual observed fractions are different estimators from the calendar-month-standardized multi-year comparisons above and should not be averaged to reproduce those comparisons.

Observed annual percentages: 2011 1.50; 2012 3.16; 2013 2.88; 2014 3.11; 2015 2.93; 2016 2.04; 2017 2.68; 2018 4.02; 2019 3.58; 2020 2.79; 2021 2.40; 2022 2.53; 2023 2.56; 2024 2.14; 2025 1.08. Annual valid-hour coverage is recorded alongside each estimate. Missing periods could contain storms; observed percentages are not gap-filled annual climatologies.

Exploratory timing check: fit monthly values using calendar-month fixed effects plus one step in mean, testing candidate first post-change years with at least three calendar years on either side. Month means are residualized from the outcome and step indicator; least-squares improvement ranks candidates. Tested 70%, 80%, 90% month coverage cutoffs, NE–SE and NE–SSE direction windows, and records ending in 2024 or 2025. All full-record variants select 2023. Omitting 2025 gives inconsistent candidate years, including upward rather than downward steps in two variants. A single-step model is therefore insufficient to establish a precise onset; 2023 is an exploratory model choice, not a statistically demonstrated change point. The search was not accompanied by a significance test or breakpoint confidence interval, and selecting among candidates introduces selection uncertainty.

A supplementary seasonal adjustment in the CSV adds each year's mean valid-month anomaly (relative to the 2011–2025 monthly climatology) to the full-year climatological mean. It assumes available-month anomalies represent unavailable months and can be unstable for rare storm conditions; it is a sensitivity check, not a reconstructed observation. The observed record suggests a reduction after active 2018–2019, a moderate plateau in 2020–2023, and marked further decline in 2024–2025. It does not support declaring a sharp 2021 transition. 2025 is the lowest observed annual rate in the 2011–2025 record analyzed here.

## Height and period jointly

height_period.py processes all valid hourly observations with the same NE–SE dominant-direction screen. Outputs are height_period_monthly.csv, height_period_annual.csv and height_period_results.txt. Five-year comparisons retain >=80%-complete months and average calendar months equally as before. Annual values weight available observations by valid hours and do not impute gaps.

Mean incoming dominant period: 9.105 s (2016–2020) versus 9.080 s (2021–2025). Time with incoming peak period >=10 s, regardless of height: 17.46% versus 17.80%; >=12 s: 5.64% versus 5.35%. Joint exceedances: Hs >3 m and Tp >=10 s, 2.004% versus 1.258% (-37.2%); Hs >3 m and Tp >=12 s, 0.842% versus 0.301% (-64.3%). Hs >2 m and Tp >=12 s declines 44.8%. Rare-event comparisons are sensitive to a small number of storms and have not been assigned confidence intervals.

Combined proxy Q = mean(I[NE–SE] * Hs^2 * Tp), calculated per observation before averaging, declines from 15.046 to 11.760 m^2 s (-21.8%). This is a relative wave-power proxy, not physical incoming energy flux at the beach: actual deep-water power uses energy period Te, not peak period Tp; finite depth and directional spreading matter, and total Hs is not an isolated incoming swell partition. No cosine projection or nearshore transformation is applied. Source for physical proportionality Hs^2 Te: https://www.energy.gov/documents/snluswectestsitecatalogue2ndeditionpart1pdf . Peak-period definition: https://www.ndbc.noaa.gov/faq/measdes.shtml .

The mean screened Hs^2 factor declines 19.1%, and its Hs^2-weighted peak period declines 3.4%; their product gives the 21.8% proxy decline. This is an algebraic decomposition, not independent causal attribution.

Annual index displayed in the response sets the mean of the five annual observed-hour Q values for 2016–2020 to 100 (baseline Q=13.46616). This differs from the month-standardized five-year baseline and is intended only to display annual variation. Values: 2011 75, 2012 105, 2013 113, 2014 100, 2015 97, 2016 81, 2017 89, 2018 138, 2019 100, 2020 93, 2021 91, 2022 86, 2023 98, 2024 96, 2025 54.

Interpretation: longer periods themselves did not broadly disappear. Large height combined with long period became substantially less common. 2018 was unusually strong; 2023–2024 recovered on the all-height combined proxy despite fewer >3 m observations, so the previous suggestion of progressively worsening overall conditions through 2024 is not supported by this broader metric. 2025 is markedly weak in both incoming period and combined proxy. No unique persistent-regime onset is established.

## NDBC spectral-energy convention table

ndbc_energy_annual.csv replaces the height-squared-times-peak-period power proxy with a direction-screened estimate of integrated spectral variance m0. NDBC reports spectral density in m^2/Hz and defines WVHT = 4 sqrt(m0), so each observation's integrated variance is inferred as WVHT^2/16. This calculation uses previously aggregated mean(I[dominant direction NE–SE] * Hs^2)/16, not the square of annual mean height. It does not download or reintegrate the original spectra, and rounding of archived WVHT affects the inferred values. Values outside the direction window contribute zero while remaining in the valid-time denominator. This preserves the earlier index's convention; it does not isolate the actual incoming fraction in mixed seas.

The index normalizes to the average of 2016–2020 annual observed-time screened m0 values, 0.086217778 m^2 = 100. It is an analyst-defined normalized index based on NDBC's spectral-energy convention, not a published NDBC index. Integrated variance describes energy content, not energy transport rate; period is therefore not multiplied into it. Actual physical energy density is proportional to rho*g*m0, and has the same normalized index for constant rho and g. No actual energy flux at the shoreline is calculated. Annual data gaps and spectral-direction limitations are unchanged. Definition sources: https://www.ndbc.noaa.gov/faq/wavecalc.shtml and https://www.ndbc.noaa.gov/faq/measdes.shtml .

## Superseding directional-spectrum refinement

The November 17, 2026 follow-up in [spectral/README.md](spectral/README.md) separates energy by frequency and reconstructed direction, then applies explicit coastline exposure masks. Its report is `../output/pdf/nh_surf_directional_report.pdf`. The earlier report remains a preliminary bulk-direction screening, not a beach-arrival estimate. In particular, the earlier 64% large/long-period decline should not be carried forward as a robust coastwide number; the revised band-height metrics, uncertainty and sheltering sensitivity are documented in the follow-up.
