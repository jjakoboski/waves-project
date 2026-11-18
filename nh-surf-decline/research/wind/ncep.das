Attributes {
    lat {
        String units "degrees_north";
        Float32 actual_range 88.542, -88.542;
        String long_name "Latitude";
        String standard_name "latitude";
        String axis "Y";
    }
    lon {
        String units "degrees_east";
        String long_name "Longitude";
        Float32 actual_range 0.0, 358.125;
        String standard_name "longitude";
        String axis "X";
    }
    time {
        String long_name "Time";
        String delta_t "0000-00-00 06:00:00";
        String standard_name "time";
        String axis "T";
        String units "hours since 1800-01-01 00:00:0.0";
        Float64 actual_range 1972320.0, 1981074.0;
        UInt32 _ChunkSizes 512;
    }
    uwnd {
        String long_name "4xDaily u-wind at 10 m";
        String units "m/s";
        Int16 precision 2;
        Int16 least_significant_digit 1;
        Int16 GRIB_id 33;
        String GRIB_name "U GRD";
        String var_desc "u-wind";
        String level_desc "10 m";
        String statistic "Individual Obs";
        String parent_stat "Other";
        Float32 missing_value -9.96921E36;
        Float32 valid_range -102.2, 102.2;
        String dataset "NCEP Reanalysis";
        Float32 actual_range -30.5, 31.0;
        UInt32 _ChunkSizes 1, 94, 192;
    }
    NC_GLOBAL {
        String Conventions "COARDS";
        String title "4x daily NMC reanalysis (2014)";
        String history "created 2022/12 by Hoop (netCDF2.3)";
        String description "Data is from NMC initialized reanalysis
(4x/day).  It consists of T62 variables interpolated to
pressure surfaces from model (sigma) surfaces.";
        String platform "Model";
        String dataset_title "NCEP-NCAR Reanalysis 1";
        String References "http://www.psl.noaa.gov/data/gridded/data.ncep.reanalysis.html";
        String _NCProperties "version=2,netcdf=4.7.0,hdf5=1.10.5,";
    }
    DODS_EXTRA {
        String Unlimited_Dimension "time";
    }
}
