# Wind direction, speed, persistence and fetch: NH wave-generation diagnostic

Calculated November 17, 2026. This study extends the wave analysis to potential generating winds. It uses complete 2011–2025 calendar years, with 2021–2025 versus 2016–2020 as the main comparison and 2011–2020 as a longer baseline. It is an exploratory diagnostic, not a calibrated wave-growth model or storm-track attribution.

## Main results

NOAA gridded wind data show a small reduction in mean speed but a larger reduction in sustained, spatially coherent wind aimed toward NH. Calendar-month-balanced results:

| Diagnostic | 2016–2020 | 2021–2025 | Relative change |
|---|---:|---:|---:|
| Mean speed over sampled offshore corridor points | 7.21 m/s | 6.96 m/s | -3.4% |
| >=10 m/s across >=200 km, 12-hour span, within 30 degrees toward NH | 1.737% | 0.995% | -42.7% |
| Same with 45-degree tolerance | 3.244% | 2.523% | -22.2% |
| >=10 m/s across >=200 km, 24-hour span, 30-degree tolerance | 0.476% | 0.121% | -74.5% |
| Same with 45-degree tolerance | 1.122% | 0.875% | -22.0% |
| >=15 m/s across >=200 km, 12-hour span, 30-degree tolerance | 0.273% | 0.083% | -69.8% |
| Same with 45-degree tolerance | 0.437% | 0.261% | -40.4% |
| >=10 m/s across >=400 km, 12-hour span, 30-degree tolerance | 0.778% | 0.436% | -44.0% |
| >=10 m/s across >=200 km, 12-hour span, no directional requirement | 30.94% | 27.72% | -10.4% |
| >=10 m/s across >=200 km, 12-hour span, aimed away from NH within 30 degrees | 9.410% | 9.888% | +5.1% |

Percentages are fractions of six-hourly analysis times at which the specified preceding wind history qualifies. They are not wind-speed changes, proportions of surfable days, or counts of independent storms. Thresholds are analyst choices and do not guarantee a particular wave height or period. The 12-hour principal diagnostic decreases 32.7% against the 2011–2020 baseline instead of 42.7% against 2016–2020.

The principal 12-hour index declines 37.7% in October–April and 58.3% in May–September. The latter is a large percentage reduction from a smaller absolute rate. Direction tolerance materially affects the estimated magnitude; claims of precisely a 74% or 70% reduction should not be presented as robust to the definition.

## Data and geometry

Data provided by NOAA PSL, Boulder, Colorado, USA, https://psl.noaa.gov . Dataset: NCEP–NCAR Reanalysis 1, six-hourly eastward and northward 10-meter wind components (`uwnd`, `vwnd`), 2011–2025. The native Gaussian grid is approximately 1.875 degrees longitude by 1.905 degrees latitude (roughly 150–210 km in the study area). These are model/reanalysis fields, not direct observed wind maps. No claim of 50-km effective resolution is made.

Source pattern:
https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/surface_gauss/uwnd.10m.gauss.2025.nc.html
(and corresponding vwnd and yearly files). Metadata are stored in ncep.das and ncep.dds. Small regional DAP2 subsets select lat indices 22–28 and lon indices 154–163. Time units are hours since 1800-01-01. All 21,916 six-hourly times are present and regularly spaced.

From an illustrative NH offshore origin at longitude -70.745, latitude 42.990 (near Jenness), eight candidate great-circle source corridors are drawn at true bearings 45, 60, 75, 90, 105, 120, 135 and 150 degrees. Corridor points extend 50–850 km offshore in 50-km steps. The long-distance bearings are updated along each WGS84 geodesic. GSHHG 2.3.7 high-resolution land geometry rejects corridors/segments whose path to the coast is blocked by land. Islands smaller than 5 km^2 are ignored for this regional wind-source test; an all-islands sensitivity was also calculated. This is not the same exposure mask used in the detailed swell analysis.

Coastline and origins use WGS84 longitude/latitude; geodesic distances and polygon areas use the WGS84 ellipsoid through PyProj.Geod. Shapely intersections in geographic coordinates are topology-only, not angular distance measurements. Geodesics are represented by the sampled points; the 5–50 km nearshore segment uses 1-km spacing. The gridded wind field is bilinearly interpolated to sample points. Interpolation does not add independent spatial resolution. Coastal mixed land/ocean grid cells are a limitation.

The widest source region extends ~850 km from NH, not the whole Atlantic. Sources farther away (including tropical cyclones), other approach directions, translating fetches, evolving wave age, and curved propagation/refraction can produce swell not represented by the diagnostic.

## Persistence and fetch definition

Wind direction is calculated FROM true north, clockwise: atan2(-u,-v). A source wind is aligned toward NH when it blows opposite the local forward bearing from NH along the ray, within 30 or 45 degrees. At every sampled point in a contiguous 200- or 400-km ocean segment, the wind must exceed the speed threshold and meet the alignment criterion at every six-hour timestamp spanning the preceding 12, 24 or 36 hours. Thus 12 hours requires three samples (t-12, t-6, t); 24 hours requires five. This demonstrates sampled persistence, not uninterrupted behavior between observations. It excludes traveling wind fields that do not persist over the same spatial segment, even though moving storms can generate strong swell.

The check is satisfied if any candidate segment on any open corridor qualifies. It does not require wind to reach the shoreline or to blow along the entire ray. The same diagnostics are computed without a direction filter and for winds aimed away from NH. Results are averaged by month, with each calendar month weighted equally in five-year comparisons. Missing values are rejected; numerical checks verify time continuity and physically plausible wind component magnitudes.

## Local buoy cross-check

NDBC standard meteorological archives provide hourly WSPD and WDIR for 44007 (Portland), 44013 (Boston) and 44005 (Gulf of Maine). Native recorded speeds are used; no historical anemometer-height homogenization was performed. Average speeds declined about 3.6% at 44007 and 8.4% at 44013, but strict NE–SE (45–135 degrees) >=10 m/s runs lasting >=12 observed hourly samples increased about 13% and 11%, respectively. These are station-specific descriptive differences, not proof of coastal wind trends. Missing hours break runs. Month comparisons require >=80% coverage. Station 44013 has substantial 2023 gaps; 44005 has too many missing years to support the headline comparison and is retained only as a diagnostic.

Hourly buoy speed is the mean reported speed within each hour; direction is the speed-weighted vector mean. A run of 12 hourly samples covers ~11 hours between its first and last timestamps, so the label `12h` describes 12 occupied hourly bins, not continuously monitored wind. This local check is therefore not identical to the gridded 12-hour-span test. Annual speed means alone miss whether a large ocean patch blows coherently toward NH.

## Relationship to swell and uncertainty

Wind setups meeting the primary diagnostic are followed 12–48 hours later by roughly 5.7 times the exposed >=8-second spectral energy of non-qualifying times, comparing within calendar month and weighting by qualifying sample counts. This association uses the preceding spectral analysis, 275 qualifying six-hour snapshots with adequate subsequent wave coverage, and at least 28 valid hours in the 37-hour follow-up window. Snapshots overlap and are NOT independent events. It is a plausibility check, not a causal coefficient or an estimate of the fraction of the swell decline explained by winds.

Annual changes do not line up perfectly: the principal wind diagnostic drops sharply in 2021–2022 and partially recovers afterward, whereas the weakest swell year is 2025. Therefore these regional wind changes cannot by themselves fully explain the wave record.

An exploratory 5,000-replicate year-block bootstrap for the strict 12-hour / 200-km / >=10 m/s diagnostic gives a 95% percentile interval of about -57% to -27%. This excludes uncertainty from coarse spatial/temporal resolution, corridor choice, interpolation, directional tolerance, reanalysis homogeneity and wind-to-wave conversion; it is not evidence of a permanent climate regime change. The large method sensitivity is explicitly reported instead of treating the strict case as uniquely correct.

## Physical interpretation and sources

Wind-wave growth depends jointly on speed, duration and fetch. A brief gust is not equivalent to a persistent storm wind over hundreds of kilometers. NOAA illustrates the scale with 30-knot wind blowing for 24 hours over 340 miles (~550 km): this can produce a very substantial sea. Our 10–15 m/s (19–29 knot), 200–400 km, 12–24 hour diagnostics probe plausible wave-generating situations, not calibrated predictions of 8-, 10- or 12-second swell.

- NOAA wave generation explanation: https://www.noaa.gov/jetstream/ocean/waves
- NOAA PSL dataset: https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html
- Example variable metadata: https://psl.noaa.gov/thredds/dodsC/Datasets/ncep.reanalysis/surface_gauss/uwnd.10m.gauss.2025.nc.html
- NDBC archive: https://www.ndbc.noaa.gov/data/historical/stdmet/
- GSHHG coast source and spectral methods: ../spectral/README.md

Scripts: buoy_winds.py; fetch_winds.py; compare_wind_swell.py; build_figures.py. Outputs: fetch_monthly.csv, fetch_annual.csv, fetch_summary.json, fetch_geometry.json, comparison.json and buoy_monthly.csv. Scientific figure: `../../output/wind/wind_fetch_and_swell.png` (also SVG). Scientific dependencies are in /tmp/nh-wave-deps, as for the spectral work.
