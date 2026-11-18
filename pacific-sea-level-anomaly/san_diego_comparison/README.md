# San Diego gauge / satellite comparison

Period: November 17, 2025–November 16, 2026, UTC. Gauge: NOAA CO-OPS station 9410170 San Diego, API location 32.7156 N, 117.1767 W. Satellite: same NOAA CoastWatch `noaacwBLENDEDsshDaily` snapshots and 0.5-degree sampled grid used in the Pacific animation. Nearest consistently valid sampled cell: 32.625 N, 117.375 W, 21.14 km from the station (WGS84 geodesic). This is the nearest animation cell, not necessarily the nearest native 0.25-degree cell or an individual satellite observation.

## Processing

- Verified hourly heights through September 30, 2026. Six-minute preliminary water levels October 1–November 16, sampled at exact UTC hours to match hourly tide predictions.
- Observations and predictions requested in meters, MSL datum, GMT. Subtract predictions at each matching hour, convert residuals to cm, then average by UTC day. Require at least 20 valid hours; all 365 days pass.
- Exclude inferred or level-limit-flagged verified hourly data. For preliminary data exclude flatness, rate-of-change, or level-limit flags. The first preliminary flag is an outlier sample count, not a binary rejection flag, and is retained. See NOAA API response documentation.
- Compare daily residuals on the 53 satellite dates. Subtract each series' separate mean over those same paired dates: satellite 10.3145 cm relative to DTU15, gauge residual 18.1495 cm. This compares variability without claiming a common absolute vertical datum.
- Gauge seven-day centered running mean is a visual guide only, with at least four daily values. All metrics and lower-panel differences use unsmoothed daily residuals.

## Results

53 pairs: Pearson correlation 0.8204; centered RMS difference 6.2982 cm; mean absolute centered difference 5.0328 cm. Verified-only subset: 46 pairs, correlation 0.4463. The strong full-period association is substantially influenced by the autumn rise, whose latest gauge measurements are preliminary. No statistical significance or independence of successive samples is asserted.

Both show higher sea levels in autumn. Comparing paired September dates with October–November dates, satellite SLA rises 17.70 cm and gauge residual rises 14.70 cm. These are sampled period differences, not sea-level trends.

## Interpretation limits

A harbor gauge measures sea level relative to local land; the satellite grid estimates offshore sea-level anomaly relative to DTU15. Tide predictions, atmospheric corrections, spatial smoothing, local coastal dynamics and harbor effects can leave differing signals. Prediction subtraction may also remove long-period harmonic components. No pressure adjustment or vertical land-motion correction was made here. This is a descriptive comparison, not a calibration, trend analysis, or absolute-datum validation.

## Sources and reproduction

- https://tidesandcurrents.noaa.gov/stationhome.html?id=9410170
- https://api.tidesandcurrents.noaa.gov/api/prod/
- https://api.tidesandcurrents.noaa.gov/api/prod/responseHelp.html
- https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsshDaily.html

Altimetry data are provided by the NOAA Laboratory for Satellite Altimetry. NOAA CoastWatch distributes these data.

Raw gauge JSON files are retained here. Satellite NetCDF chunks, source metadata and download URLs are retained in ../pacific_sla. Run compare.py with Python plus numpy, pandas, netCDF4, pyproj and matplotlib. Outputs include the comparison PNG, paired data CSV, daily gauge CSV and statistics JSON. Original gauge flags remain in the raw JSON files.
