Attributes {
    sourceFilename {
        String long_name "source file name";
        String _FillValue "_";
        DODS {
            Int32 strlen 30;
            String dimName "sourceNameLength";
        }
    }
    waveTime {
        String long_name "UTC sample start time";
        String standard_name "time";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String axis "T";
        String coverage_content_type "coordinate";
        String bounds "waveTimeBounds";
        String comment "Spectral processing performed on 1600-second samples specified by waveTimeBounds.";
    }
    waveTimeBounds {
        String long_name "time cell bounds";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String coverage_content_type "auxiliaryInformation";
    }
    waveFlagPrimary {
        String _Unsigned "false";
        String long_name "primary wave QC flag";
        Int16 _FillValue -127;
        String standard_name "status_flag";
        Byte valid_min 1;
        Byte valid_max 9;
        Byte flag_values 1, 2, 3, 4, 9;
        String flag_meanings "good not_evaluated questionable bad missing";
        String reference "Ocean Data Standards, UNESCO 2013 - IOC Manuals and Guides, 54, Volume 3 Version 1";
        String ancillary_variables "waveFlagSecondary";
        String coverage_content_type "qualityInformation";
    }
    waveFlagSecondary {
        String _Unsigned "false";
        String long_name "secondary wave QC flag";
        Int16 _FillValue -127;
        Byte valid_min 0;
        Byte valid_max 19;
        Byte flag_values 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19;
        String flag_meanings "unspecified sensor_issues Hs_out_of_range Tp_out_of_range Ta_out_of_range elevated_check_factors Hs_spike Ta_spike low_freq_energy_spike excessive_low_freq_energy hf_transmission_errors_fixed hf_transmission_errors_present directional_coeffs_out_of_range incomplete_spectrum spectrum_layout_modified too_few_segments inclination_off max_energy_at_highest_freq freq_over_hull_response_limit a0_hs_discrepancy";
        String reference "http://cdip.ucsd.edu/documentation";
        String coverage_content_type "qualityInformation";
    }
    waveHs {
        String long_name "significant wave height";
        String units "meter";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_significant_height";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 20.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
        String ncei_name "WAVE HEIGHT - SIGNIFICANT";
    }
    waveTp {
        String long_name "peak wave period";
        String units "second";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_period_at_variance_spectral_density_maximum";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 40.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
        String ncei_name "WAVE - PEAK PERIOD";
    }
    waveTa {
        String long_name "average wave period";
        String units "second";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_mean_period_from_variance_spectral_density_first_frequency_moment";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 40.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
        String ncei_name "WAVE PERIOD - AVERAGE";
        String additional_processing "Calculated from the full-spectrum, buoy-returned energy density values.";
    }
    waveDp {
        String long_name "peak wave direction";
        String units "degreeT";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_from_direction_at_variance_spectral_density_maximum";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 360.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
        String ncei_name "WAVE DIRECTION";
        String additional_processing "Magnetic declination - INT(metaDeclination) - added to buoy-returned direction to shift to degrees true.";
    }
    wavePeakPSD {
        String long_name "peak wave power spectral density";
        String units "m*m/hertz";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_energy_at_variance_spectral_density_maximum";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 5000.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
    }
    waveTz {
        String long_name "spectral zero-upcross wave period";
        String units "second";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_mean_period_from_variance_spectral_density_second_frequency_moment";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 40.0;
        String ancillary_variables "waveFlagPrimary waveFlagSecondary";
    }
    waveSourceIndex {
        String long_name "source file index";
        Int32 _FillValue -99999;
    }
    waveFrequency {
        String long_name "band center frequency";
        String units "hertz";
        String standard_name "wave_frequency";
        String bounds "waveFrequencyBounds";
    }
    waveFrequencyBounds {
        String long_name "frequency cell bounds";
        String units "hertz";
    }
    waveFrequencyFlagPrimary {
        String _Unsigned "false";
        String long_name "primary waveFrequency QC flag";
        Int16 _FillValue -127;
        String standard_name "status_flag";
        Byte valid_min 1;
        Byte valid_max 9;
        Byte flag_values 1, 2, 3, 4, 9;
        String flag_meanings "good not_evaluated questionable bad missing";
        String reference "Ocean Data Standards, UNESCO 2013 - IOC Manuals and Guides, 54, Volume 3 Version 1";
        String ancillary_variables "waveFrequencyFlagSecondary";
        String coverage_content_type "qualityInformation";
    }
    waveFrequencyFlagSecondary {
        String _Unsigned "false";
        String long_name "secondary waveFrequency QC flag";
        Int16 _FillValue -127;
        Byte valid_min 0;
        Byte valid_max 2;
        Byte flag_values 0, 1, 2;
        String flag_meanings "unspecified out_of_range above_hull_response_limit";
        String reference "http://cdip.ucsd.edu/documentation";
        String coverage_content_type "qualityInformation";
    }
    waveBandwidth {
        String long_name "bandwidth";
        String units "hertz";
        Float32 _FillValue -999.99;
        String ncei_name "WAVE ENERGY - WIDTH OF SPECTRAL BANDS";
    }
    waveEnergyDensity {
        String long_name "band energy density";
        String units "meter^2 second";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_variance_spectral_density";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE ENERGY - SPECTRAL VALUE";
    }
    waveMeanDirection {
        String long_name "band mean direction";
        String units "degreeT";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_from_direction";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 360.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE DIRECTION - AVERAGE";
        String additional_processing "Magnetic declination (metaDeclination) added to buoy-returned direction to shift to degrees true.";
    }
    waveA1Value {
        String long_name "band a1 Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE DATA - ANGULAR FOURIER COEFFICIENTS";
        String additional_processing "Calculated relative to true north from the buoy-returned mean dir, spread, m2, and n2.";
    }
    waveB1Value {
        String long_name "band b1 Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE DATA - ANGULAR FOURIER COEFFICIENTS";
        String additional_processing "Calculated relative to true north from the buoy-returned mean dir, spread, m2, and n2.";
    }
    waveA2Value {
        String long_name "band a2 Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE DATA - ANGULAR FOURIER COEFFICIENTS";
        String additional_processing "Calculated relative to true north from the buoy-returned mean dir, spread, m2, and n2.";
    }
    waveB2Value {
        String long_name "band b2 Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
        String ncei_name "WAVE DATA - ANGULAR FOURIER COEFFICIENTS";
        String additional_processing "Calculated relative to true north from the buoy-returned mean dir, spread, m2, and n2.";
    }
    waveCheckFactor {
        String long_name "band check factor (inverse of wave ellipticity)";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 2.55;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
    }
    waveSpread {
        String long_name "band directional spread";
        String units "degree";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_wave_directional_spread";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min 0.0;
        Float32 valid_max 90.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
    }
    waveM2Value {
        String long_name "band centered sine Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
    }
    waveN2Value {
        String long_name "band centered cosine Fourier coefficient";
        Float32 _FillValue -999.99;
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -1.0;
        Float32 valid_max 1.0;
        String ancillary_variables "waveFlagPrimary waveFrequencyFlagPrimary waveFlagSecondary waveFrequencyFlagSecondary";
    }
    sstTime {
        String long_name "UTC sample time";
        String standard_name "time";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String axis "T";
        String coverage_content_type "coordinate";
        String bounds "sstTimeBounds";
    }
    sstTimeBounds {
        String long_name "time cell bounds";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String coverage_content_type "auxiliaryInformation";
    }
    sstFlagPrimary {
        String _Unsigned "false";
        String long_name "primary sst QC flag";
        Int16 _FillValue -127;
        String standard_name "status_flag";
        Byte valid_min 1;
        Byte valid_max 9;
        Byte flag_values 1, 2, 3, 4, 9;
        String flag_meanings "good not_evaluated questionable bad missing";
        String reference "Ocean Data Standards, UNESCO 2013 - IOC Manuals and Guides, 54, Volume 3 Version 1";
        String ancillary_variables "sstFlagSecondary";
        String coverage_content_type "qualityInformation";
    }
    sstFlagSecondary {
        String _Unsigned "false";
        String long_name "secondary sst QC flag";
        Int16 _FillValue -127;
        Byte valid_min 0;
        Byte valid_max 7;
        Byte flag_values 0, 1, 2, 3, 4, 5, 6, 7;
        String flag_meanings "unspecified sensor_issues SST_out_of_range SST_spike SST_max_change_exceeded hf_transmission_errors_fixed hf_transmission_errors_present reference_temperature_off";
        String reference "http://cdip.ucsd.edu/documentation";
        String coverage_content_type "qualityInformation";
    }
    sstSeaSurfaceTemperature {
        String long_name "sea surface temperature";
        String units "Celsius";
        Float32 _FillValue -999.99;
        String standard_name "sea_surface_temperature";
        String coordinates "metaStationLatitude metaStationLongitude";
        String grid_mapping "metaGridMapping";
        Float32 valid_min -5.0;
        Float32 valid_max 46.15;
        String ancillary_variables "sstFlagPrimary sstFlagSecondary";
        String ncei_name "SEA SURFACE TEMPERATURE";
        String cell_methods "sstTime: point";
    }
    sstSourceIndex {
        String long_name "source file index";
        Int32 _FillValue -99999;
    }
    sstReferenceTemp {
        String long_name "reference temperature";
        String units "Celsius";
        Float32 _FillValue -999.99;
    }
    gpsTime {
        String long_name "UTC sample time";
        String standard_name "time";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String axis "T";
        String coverage_content_type "coordinate";
        String bounds "gpsTimeBounds";
    }
    gpsTimeBounds {
        String long_name "time cell bounds";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String coverage_content_type "auxiliaryInformation";
    }
    gpsStatusFlags {
        String _Unsigned "false";
        String long_name "gps data flags";
        Int16 _FillValue -127;
        Byte flag_masks 1, 2, 4, 8;
        String flag_meanings "module_ok new_fix figure_of_merit hf_transmission_error";
        String comment "Good GPS positions will have module_ok and new_fix set, i.e. gpsStatusFlags=3. All other positions should be ignored. Note that some records with gpsStatusFlags=3 may also be erroneous, these values are not subject to any quality control.";
    }
    gpsLatitude {
        String long_name "buoy latitude";
        String units "degrees_north";
        Float32 _FillValue -999.99;
        Float32 valid_min -90.0;
        Float32 valid_max 90.0;
        String ncei_name "LATITUDE";
        String cell_methods "gpsTime: point";
        String ancillary_variables "gpsStatusFlags";
    }
    gpsLongitude {
        String long_name "buoy longitude";
        String units "degrees_east";
        Float32 _FillValue -999.99;
        Float32 valid_min -180.0;
        Float32 valid_max 180.0;
        String ncei_name "LONGITUDE";
        String cell_methods "gpsTime: point";
        String ancillary_variables "gpsStatusFlags";
    }
    gpsSourceIndex {
        String long_name "source file index";
        Int32 _FillValue -99999;
    }
    dwrTime {
        String long_name "UTC sample time";
        String standard_name "time";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String axis "T";
        String coverage_content_type "coordinate";
        String bounds "dwrTimeBounds";
    }
    dwrTimeBounds {
        String long_name "time cell bounds";
        String units "seconds since 1970-01-01 00:00:00 UTC";
        String calendar "standard";
        String coverage_content_type "auxiliaryInformation";
    }
    dwrSourceIndex {
        String long_name "source file index";
        Int32 _FillValue -99999;
    }
    dwrBatteryLevel {
        String long_name "battery level";
        Int32 _FillValue -99999;
        Int32 valid_min 0;
        Int32 valid_max 7;
    }
    dwrZAccelerometerOffset {
        String long_name "vertical accelerometer offset";
        String units "m/s^2";
        Float32 _FillValue -999.99;
    }
    dwrXAccelerometerOffset {
        String long_name "x-axis accelerometer offset";
        String units "m/s^2";
        Float32 _FillValue -999.99;
    }
    dwrYAccelerometerOffset {
        String long_name "y-axis accelerometer offset";
        String units "m/s^2";
        Float32 _FillValue -999.99;
    }
    dwrOrientation {
        String long_name "buoy orientation";
        String units "degrees";
        Float32 _FillValue -999.99;
        String standard_name "platform_orientation";
    }
    dwrInclination {
        String long_name "magnetic inclination";
        String units "degrees";
        Float32 _FillValue -999.99;
    }
    dwrBatteryWeeksOfLife {
        String long_name "battery weeks of life";
        String units "weeks";
        Int32 _FillValue -99999;
    }
    metaDeployLatitude {
        String standard_name "latitude";
        String units "degrees_north";
        Float32 valid_min -90.0;
        Float32 valid_max 90.0;
        String coverage_content_type "referenceInformation";
        String ncei_name "LATITUDE";
        String long_name "deployment latitude";
    }
    metaDeployLongitude {
        String standard_name "longitude";
        String units "degrees_east";
        Float32 valid_min -180.0;
        Float32 valid_max 180.0;
        String coverage_content_type "referenceInformation";
        String ncei_name "LONGITUDE";
        String long_name "deployment longitude";
    }
    metaWaterDepth {
        String standard_name "sea_floor_depth_below_sea_surface";
        String long_name "water depth";
        String units "meter";
        Float32 _FillValue -999.99;
        String ncei_name "DEPTH - BOTTOM";
        String coverage_content_type "referenceInformation";
    }
    metaDeclination {
        String long_name "magnetic declination";
        String units "degree";
    }
    metaStationName {
        String long_name "station name";
        String cf_role "timeseries_id";
        DODS {
            Int32 strlen 31;
            String dimName "metaStationNameLength";
        }
    }
    metaStationLatitude {
        String standard_name "latitude";
        String units "degrees_north";
        Float32 valid_min -90.0;
        Float32 valid_max 90.0;
        String axis "Y";
        String coverage_content_type "coordinate";
        String ncei_name "LATITUDE";
        String long_name "station average latitude";
        String comment "Averaged over all records. Record-specific deployment positions can be obtained from metaDeployLatitude and metaDeployLongitude as indexed by waveSourceIndex, sstSourceIndex, etc.";
    }
    metaStationLongitude {
        String standard_name "longitude";
        String units "degrees_east";
        Float32 valid_min -180.0;
        Float32 valid_max 180.0;
        String axis "X";
        String coverage_content_type "coordinate";
        String ncei_name "LONGITUDE";
        String long_name "station average longitude";
        String comment "Averaged over all records. Record-specific deployment positions can be obtained from metaDeployLatitude and metaDeployLongitude as indexed by waveSourceIndex, sstSourceIndex, etc.";
    }
    metaPlatform {
        String long_name "platform_attributes";
        String make_model "Multiple sensors possibly used. Please refer to per-deployment datasets.";
        String documentation_url "http://datawell.nl";
        String mooring "Datawell-compliant";
        DODS {
            Int32 strlen 0;
        }
    }
    metaInstrumentation {
        String long_name "instrumentation_attributes";
        String make_model "Multiple sensors possibly used. Please refer to per-deployment datasets.";
        String documentation_url "http://datawell.nl";
        String mooring "Datawell-compliant";
        DODS {
            Int32 strlen 0;
        }
    }
    metaGridMapping {
        String grid_mapping_name "latitude_longitude";
        Float32 longitude_of_prime_meridian 0.0;
        Float64 semi_major_axis 6378137.0;
        Float64 inverse_flattening 298.257223563;
        String coverage_content_type "referenceInformation";
        DODS {
            Int32 strlen 0;
        }
    }
    NC_GLOBAL {
        String naming_authority "edu.ucsd.cdip";
        String keywords_vocabulary "Global Change Master Directory (GCMD) Earth Science Keywords";
        String date_created "2026-01-29T04:52:23Z";
        String date_issued "2026-01-29T04:52:23Z";
        String date_modified "2026-01-29T04:52:23Z";
        String creator_name "Coastal Data Information Program, SIO/UCSD";
        String creator_url "http://cdip.ucsd.edu";
        String creator_email "www@cdip.ucsd.edu";
        String creator_institution "Scripps Institution of Oceanography, UCSD";
        String creator_country "USA";
        String creator_sector "academic";
        String publisher_name "Coastal Data Information Program, SIO/UCSD";
        String publisher_url "http://cdip.ucsd.edu";
        String publisher_email "www@cdip.ucsd.edu";
        String publisher_country "USA";
        String publisher_institution "Scripps Institution of Oceanography, UCSD";
        String institution "Scripps Institution of Oceanography, University of California San Diego";
        String project "Coastal Data Information Program (CDIP)";
        String processing_level "QA/QC information available at http://cdip.ucsd.edu/documentation";
        String standard_name_vocabulary "CF Standard Name Table v79";
        String Conventions "ACDD-1.3, CF-1.8, IOOS-1.2";
        String license "These data may be redistributed and used without restriction.";
        String cdm_data_type "Station";
        String featureType "timeSeries";
        String ncei_template_version "NCEI_NetCDF_TimeSeries_Orthogonal_Template_v2.0";
        String references "http://cdip.ucsd.edu/documentation";
        String uuid "83F91C39-2EC4-46E9-9CAA-35B1BD24B021";
        String title "Directional wave and sea surface temperature measurements collected in situ by Datawell Waverider buoys located near JEFFREYS LEDGE, NH from 2008/09/11 to 2025/08/08.";
        String summary "Directional wave and sea surface temperature measurements collected in situ by Datawell Waverider buoys located near JEFFREYS LEDGE, NH from 2008/09/11 to 2025/08/08. This dataset includes publicly-released data only, excluding all records flagged bad by quality control procedures. A total of 286669 wave samples were analyzed for this area, where the water depth is approximately 77 to 80 meters.";
        String keywords "EARTH SCIENCE, OCEANS, OCEAN WAVES, GRAVITY WAVES, WIND WAVES, SIGNIFICANT WAVE HEIGHT, WAVE FREQUENCY, WAVE PERIOD, WAVE SPECTRA, OCEAN TEMPERATURE, SEA SURFACE TEMPERATURE, WATER TEMPERATURE, OCEAN, ATLANTIC OCEAN, NORTH ATLANTIC OCEAN";
        String id "CDIP_160p1_20080911-20250808_historic";
        String history "2026-01-29T04:52:23Z: dataset created; user, program, arguments: uproc, wnc_aggregate_hist v1.0, 160p1. If date_modified is after date_created, contact CDIP for details of changes.";
        String comment "Multiple deployments may be included in this dataset. Please refer to the per-deployment datasets - as referenced by sourceFilename and the xxxSourceIndex variables - for more complete metadata. All values are decoded directly from the instruments in accordance with the manufacturers documentation EXCEPT for those with the attribute :additional_processing which describes further data handling performed by CDIP.";
        String acknowledgment "CDIP is primarily supported by the U.S. Army Corps of Engineers (USACE). Station partner: UNH ; Field operator: UNH";
        String metadata_link "http://cdip.ucsd.edu/metadata/160p1";
        String infoUrl "http://cdip.ucsd.edu/metadata/160p1";
        String contributor_name "UNH, UNH/USACE, CDIP";
        String contributor_role "station operation, station funding, data management";
        Float32 geospatial_lat_min 42.794792;
        Float32 geospatial_lat_max 42.803;
        String geospatial_lat_units "degrees_north";
        Float32 geospatial_lat_resolution 1.0E-4;
        Float32 geospatial_lon_min -70.17474;
        Float32 geospatial_lon_max -70.16515;
        String geospatial_lon_units "degrees_east";
        Float32 geospatial_lon_resolution 1.0E-4;
        Float32 geospatial_vertical_min 0.0;
        Float32 geospatial_vertical_max 0.0;
        String geospatial_vertical_units "meters";
        String geospatial_vertical_origin "sea surface";
        String geospatial_vertical_positive "up";
        Float32 geospatial_vertical_resolution 1.0;
        String time_coverage_start "2008-09-11T00:00:00Z";
        String time_coverage_end "2025-08-08T19:59:59Z";
        String time_coverage_duration "P0882W1DT20H";
        String time_coverage_resolution "PT30M";
        String source "insitu observations";
        String platform "metaPlatform";
        String instrument "metaInstrumentation";
    }
}
