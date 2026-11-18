# Pacific sea level anomaly animation

53 snapshots, November 17, 2025–November 16, 2026. NOAA CoastWatch dataset `noaacwBLENDEDsshDaily`, variable `sla`, sampled every seventh available daily field, plus the latest field. June 1, 2026 is absent from the source; the weekly sequence shifts by one day after that gap. These are snapshots, not weekly means.

Source: https://coastwatch.noaa.gov/erddap/griddap/noaacwBLENDEDsshDaily.html

Anomalies are relative to the DTU15 mean sea surface. Source meters are converted to centimeters. The fixed diverging scale is −60 to +60 cm, with saturated colors beyond that range. Land is beige-gray; missing ocean data are blue-gray. This is a near-real-time satellite-derived, optimally interpolated product, not a coastal flood forecast.

The native 0.25° grid is subsampled every second point (0.5°), without spatial averaging. The display covers 120°E–70°W, 60°S–65°N. Some marginal seas are included. Geographic longitude/latitude coordinates are explicitly transformed with Cartopy PlateCarree to a Pacific-centered equirectangular map. Eastern longitudes are shifted by 360° to maintain continuity at the dateline. No distance or area measurements are made. Natural Earth 1:110m land outlines provide geographic context.

Downloads were split into small time chunks after full-year requests timed out. `urls.txt` records each successful request; `source_metadata.json` preserves the source metadata; `available_dates.csv` preserves available daily dates. NetCDF chunks include all longitudes to simplify bounded requests; the render script selects the Pacific domain. `manifest.json` records actual rendered dates and configuration.

Reproduce with Python, numpy, matplotlib, cartopy, netCDF4, Pillow and ffmpeg:

    python download.py
    python render.py

Adjust the ffmpeg executable path in render.py for your system. Outputs are looping GIF, H.264 MP4, and PNG stills. Each frame lasts 0.2 seconds (5 frames per second).
