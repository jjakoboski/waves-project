# NH swell spectra and direct coastal exposure

Analysis completed November 17, 2026. This is a refinement of the earlier dominant-direction screen, not a nearshore wave model. Results describe offshore spectral energy in directions with a direct open-water approach to three representative offshore NH points. They do not measure surf heights at beaches.

## Data and sampling

CDIP station 160p1 is NDBC 44098 (Jeffreys Ledge). The quality-controlled historic NetCDF archive ends August 8, 2025. The current deployment provides August 19–December 31, 2025. Use only primary quality flag 1 and good frequency bands. Archived waves have 64 frequency bins; the replacement buoy has 100. Actual frequency centers/bandwidths are read separately and partial cells integrated at the 8-, 10- and 12-second limits. Flagged 0.025/0.030-Hz bands are excluded, so analyzed swell extends to roughly 30.8 seconds, not infinite period.

Data requests select every second (normally half-hourly) record, yielding approximately hourly sampling. Records falling in the same UTC hour are averaged. 127,264 valid hourly records cover 2011–2025. Missing hours are not filled. See annual_metrics.csv for coverage, roughly 88–100%. Comparisons retain months with >=80% hourly coverage; monthly means are averaged by calendar month across available years, then equally across the twelve months. This improves coverage relative to the prior NDBC bulk archive and changes the sample as well as the method.

Sources:
- Historic dataset: https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/archive/160p1/160p1_historic.nc.html
- Current deployment: https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/160p1_rt.nc.html
- CDIP directional spectrum method: https://cdip.ucsd.edu/m/products/polar_spectrum/?stn=160p1
- CDIP data access and quality caveat: https://www.cdip.ucsd.edu/m/documents/data_access.html

## Directional reconstruction

A 2D frequency/direction spectrum is estimated with the Burg maximum-entropy method (Lygre & Krogstad 1986) from E(f), a1, b1, a2, b2 at each observation. This uses the measured first two angular Fourier moments; it is not a directly observed unique directional spectrum. Separate wave systems with similar frequencies can remain ambiguous. No watershed event partitioning or count of independent swells is attempted.

c1=a1+i*b1; c2=a2+i*b2; phi1=(c1-c2*conj(c1))/(1-|c1|^2); phi2=c2-phi1*c1. D(theta) is proportional to Re(1-phi1*conj(c1)-phi2*conj(c2))/|1-phi1*exp(-i theta)-phi2*exp(-2i theta)|^2. Normalize over 360 degrees. CDIP coefficients use degrees FROM true north, clockwise. The mean angle from a1/b1 was checked against CDIP's mean-direction variable (max difference <0.00002 degree for the 100-record check).

Numerical integration uses 1-degree bins, adaptively refined to 0.1 or 0.02 degrees for narrow spectra whose reconstructed angular moments deviate by >0.001. Maximum residual is <0.001; 1,065 frequency-observation pairs required refinement. Integrating D over all directions returns one. Historic swell-band energy is always below total energy inferred from Hs; maximum ratio 0.963. Bad directional moment rows are excluded. Full numerical validation is in validation.json.

Method reference and checked implementation:
- https://journals.ametsoc.org/view/journals/phoc/16/12/1520-0485_1986_016_2052_meeotd_2_0_co_2.xml
- https://wavespotter.github.io/ocean-science-utilities/wavespectra/estimators/mem.html

## Coastal exposure and CRS

GSHHG 2.3.7 high-resolution level-1 land polygons, derived from the historical World Vector Shoreline, are used for a regional geometric screening. They are not a surveyed modern local shoreline. Source CRS: WGS84 longitude/latitude (EPSG:4326), with longitude-first API order. Intersection/buffering CRS: WGS84 UTM zone 19N (EPSG:32619), meters. Rays follow WGS84 ellipsoidal geodesics, densified every 1 km. Round-trip coordinate checks pass below 1e-8 degree. No elevations or vertical datum are used.

Representative offshore points (not exact surf breaks): Hampton (-70.780, 42.910); Jenness (-70.745, 42.990); Wallis (-70.695, 43.040). All are verified offshore against the land polygons. The central case excludes direction bins with land anywhere along a 100-km ray extending FROM each point toward the wave source. This yields different masks for each point, including shadows from Cape Ann and the Isles of Shoals. Applying these masks to the buoy spectrum assumes the offshore directional wave field is spatially representative across the region. Waves need not literally pass through the buoy before arriving at a site.

Sensitivity cases: ray lengths 50 and 150 km; land expanded by 500 m; islands smaller than 5 km^2 treated as transparent. The transparent-island case is an illustrative sensitivity, not a physical diffraction model or guaranteed upper bound. Rays, masks, sites and metadata are stored in exposure_masks.npz and exposure_summary.json. Coastal source: https://github.com/GenericMappingTools/gshhg-gmt/releases/download/2.3.7/gshhg-shp-2.3.7.zip . GSHHG background: https://www.soest.hawaii.edu/pwessel/gshhs/index.html .

## Metrics and comparability

m0_T = integral of E(f)*D(f,theta)*exposure(theta) over good frequency bands f<=1/T and all directions. Units m^2. Physical energy per unit sea area is proportional to rho*g*m0_T. Equivalent swell-band significant height H_T=4*sqrt(m0_T). Thus `H_10 >3 m` means the energy in exposed >=10-second components alone produces an equivalent significant height >3 m. It is NOT the old condition `total Hs >3 m and dominant period >=10 s`. Nor is it breaking-wave height. Direct comparisons of old and new percentage magnitudes are not apples-to-apples.

Regional summaries equally average the three site-specific mean energies or exceedance-time fractions; they are representative exposure comparisons, not a coastline-length-weighted census. Annual index baseline is the mean of the 2016–2020 annual regional m0_8 values, defined as 100. Annual indices use observed hours, not the month-balanced five-year estimator.

Main 100-km all-island result, 2021–2025 versus 2016–2020: >=8-second swell energy -12.5%; >=10-second energy -13.1%; >=12-second energy -17.3%. Site-specific >=8-second changes range -10.4% to -13.5%. Equivalent H8 >3 m time declines 25.8%; H10 >3 m declines 33.0%; H12 >3 m declines 27.5%; H12 >2 m declines 49.2%. Under the transparent-small-island case, respective changes are -12.9%, -13.9%, -18.5%, -26.9%, -36.8%, -37.9%, -51.3%.

The rare H12 >3 m condition is NOT uniformly declining at all sites: the strict Jenness island mask gives an increase from a very low baseline. Small changes in sheltering substantially change individual-site exceedances. The earlier report's 64% decline must not be carried forward as a robust coastwide estimate.

## Uncertainty and interpretation

A year-block bootstrap resamples years within each five-year period, preserves available months, and repeats calendar-month balancing. The regional >=8-second energy change has an approximate percentile 95% interval of -35% to +10% (3,992 valid draws out of 4,000). This is exploratory with only five years per group. Exceedance intervals are wider and also include zero. It does not include uncertainty from instrument changes, missing storms, directional reconstruction or coastal modeling. Model-sensitivity ranges are not confidence intervals.

2025 is weak before the August buoy replacement: January–July >=8-second exposed energy is about 65% below the corresponding 2016–2020 calendar months. This reduces, but does not eliminate, concern that the replacement alone explains 2025. A full sensor-homogeneity audit was not performed.

The analysis supports a descriptive reduction in potentially incoming swell energy and larger long-period conditions. It does not establish a permanent regime shift, storm-track cause, or anthropogenic attribution. Bathymetry, depth refraction, shoaling, diffraction around islands, currents, tides, local wind growth and shoreline breaking are not simulated. A validated SWAN or equivalent nearshore hindcast would be needed to estimate actual beach arrival and surf height.

## Files and reproduction

- dap_read.py parses downloaded DAP2 arrays and validates byte counts.
- coastal_exposure.py builds geometric masks and records CRS and ray metadata.
- analyze_spectra.py reconstructs spectra, validates moments and writes hourly/monthly/annual metrics.
- summarize.py produces report_results.json, coast_summary_annual.csv and year-bootstrap comparisons.
- Dependencies installed temporarily in /tmp/nh-wave-deps; run with PYTHONPATH pointing there and the bundled Python interpreter. Scientific packages include numpy, shapely, pyproj, pyshp and matplotlib.
- The earlier full-spectrum downloads named waveEnergyDensity.dods and waveA*/waveB*/waveMeanDirection.dods were interrupted and are NOT used. Used downloads are coords.dods, rt_coords.dods, swell_*.dods, quality.dods, late2025_fullswell.dods and check_direction.dods.
