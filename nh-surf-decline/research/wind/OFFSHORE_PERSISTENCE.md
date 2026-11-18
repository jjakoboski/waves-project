# Offshore wind persistence: NH, 2011–2025

## Finding
No broad increase in persistent eastward winds appears in the 2021–2025 average versus 2016–2020. Stronger extremes and individual years differ. The 2025 annual 24-hour/10 m/s diagnostic is the highest of these 15 years; 2022 and 2023 are weak. This is descriptive evidence, not causal attribution or a statistically established trend.

## Method
See README.md for data acquisition and open-water corridor geometry. NOAA PSL NCEP–NCAR Reanalysis 1 six-hourly 10 m wind components were interpolated to the existing eight offshore corridors (bearings 45–150 degrees from NH), sampled every 50 km out to 850 km where land permits. Native resolution is roughly 150–210 km; interpolation does not create finer meteorological information.

Define offshore as wind FROM 225–315 degrees (SW through W to NW), thus blowing toward NE through E to SE. Primary diagnostic also requires wind travel within 45 degrees of the local outward corridor bearing. At every sampled point on at least one contiguous 200 km segment, speed and direction must qualify at every six-hourly observation over the preceding duration. A 24-hour interval requires five snapshots. Count only qualifying endpoints, not the full preceding episode. These fractions are not counts of independent storms and do not establish continuous conditions between observations. Each endpoint may qualify via a different corridor, but its preceding interval must qualify along a single segment. This is a spatial persistence proxy, not a wave-growth model or an exact wind-aligned fetch calculation.

Five-year results weight each calendar month equally. Annual results use all six-hourly observations. 2026 is excluded. Missing data break buoy persistence windows. Buoy monthly comparisons require at least 80% valid hourly coverage, with eligible complete windows as denominators. Buoy sensor heights have not been homogenized.

## Main comparison
Percent of qualifying observations, 2016–2020 -> 2021–2025, primary 200 km/45-degree diagnostic:

| Speed | Duration | Earlier % | Recent % | Relative change |
|---|---:|---:|---:|---:|
| >=5 m/s | 24 h | 10.747 | 10.461 | -2.7% |
| >=10 m/s | 12 h | 7.715 | 7.150 | -7.3% |
| >=10 m/s | 24 h | 3.223 | 3.072 | -4.7% |
| >=10 m/s | 48 h | 0.580 | 0.386 | -33.5% |
| >=15 m/s | 24 h | 0.243 | 0.351 | +44.7% |

The rare >=15 m/s, 24-hour category increased, but from a small baseline. With 30-degree alignment the >=10 m/s, 24-hour change is +6.4%; with fixed westerly sector only, no corridor-alignment test, it is -15.1%. Thus even the sign of this moderate change depends on geometry. The earlier ray-relative 'away' result (+23% for 24 hours) used a different definition, allowing directions outside the fixed western sector; it should not be described as a general increase in westerly persistence.

Local checks are mixed: >=10 m/s westerlies sustained 24 hours increased at Portland 44007 from 0.052% to 0.196% of eligible observations, but Boston 44013 changed from 0.653% to 0.640%. These are rare events and geographically different measurements, not direct NH beach observations.

## Interpretation
The results do not support a sustained increase in eastward wind persistence as the sole explanation of lower NH surf. The prior analysis of reduced inward-directed generating setups is a separate hypothesis. Offshore wind-generated waves travel away from NH; do not count them as incoming surf. This diagnostic neither calculates attenuation of existing incoming swell nor attributes the regional pattern to climate circulation changes.

Wave growth depends on wind speed, duration and fetch; remotely generated swell can travel beyond its generating winds. Source: https://www.noaa.gov/jetstream/ocean/waves

Data provided by NOAA PSL, Boulder, Colorado, USA: https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html

Reproducible code: offshore_persistence.py and plot_offshore.py. Full results: offshore_annual.csv, offshore_monthly.csv, offshore_summary.json, offshore_buoy_monthly.csv. Figure: ../../output/wind/offshore_persistence.png
