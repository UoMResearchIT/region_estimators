# region_estimators package

[![Build Status](https://travis-ci.org/UoMResearchIT/region_estimators.svg?branch=master)](https://travis-ci.org/UoMResearchIT/region_estimators)

region_estimators is a Python library to calculate regional estimations of scalar quantities, based on some known scalar quantities at specific locations.
For example, estimating the NO2 (pollution) level of a postcode/zip region, based on site data nearby.
This first version of the package is initialised with 2 estimation methods:
1. ConcentricRegions: look for actual data points in gradually wider rings, starting with sites within the region, and then working in rings outwards, until sites are found. If more than one site is found at the final stage, it takes the mean.
2. Simple Distance measure: This is a very basic implementation... Find the nearest site to the region and use that value.
If sites exist within the region, take the mean.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install region_estimators.

```bash
pip install shapely
pip install pandas
pip install geopandas
pip install region_estimators
```

## Usage

```python
>>> from shapely import wkt
>>> import pandas as pd
>>> from region_estimators import RegionEstimatorFactory


# Prepare input files  (For sample input files, see the 'sample_input_files' folder)
>>> df_regions = pd.read_csv('/path/to/file/df_regions.csv', index_col='region_id')
>>> df_sites = pd.read_csv('/path/to/file/df_sites.csv', index_col='site_id')
>>> df_actuals = pd.read_csv('/path/to/file/df_actuals.csv')

# Convert the regions geometry column from string to wkt format using wkt
>>> df_regions['geometry'] = df_regions.apply(lambda row: wkt.loads(row.geometry), axis=1)

# Create estimator, the first parameter is the estimation method.
>>> estimator = RegionEstimatorFactory.region_estimator('concentric-regions', df_sites, df_regions, df_actuals)

# Make estimations
>>> estimator.get_estimations('urtica', 'AB', '2017-07-01')
>>> estimator.get_estimations('urtica', None, '2018-08-15') 	# Get estimates for all regions
>>> estimator.get_estimations('urtica', 'AB', None)	  	# Get estimates for all timestamps
>>> estimator.get_estimations('urtica', None, None) 		# Get estimates for all regions and timestamps

# Convert dataframe result to (for example) a csv file:
>>> df_region_estimates = estimator.get_estimations('urtica', None, '2018-08-15')
>>> df_region_estimates.to_csv('/path/to/file/df_urtica_2018-08-15_estimates.csv')




##### Details of region_estimators classes / methods used above: #####

'''
    # Call RegionEstimatorFactory.region_estimator

    # Reguired inputs:

    # 	method_name (string): 	the estimation method. For example, in the first version
    # 				the options are 'concentric-regions' or 'distance-simple'


    # 	3 pandas.Dataframe objects:  (For sample input files, see the 'sample_input_files' folder)


    sites: list of sites as pandas.DataFrame (one row per site)
	    Required columns:
                'site_id' (INDEX): identifier for site (must be unique to each site)
                'latitude' (numeric): latitude of site location
                'longitude' (numeric): longitude of site location
        Optional columns:
                'name' (string): Human readable name of site

    regions: list of regions as pandas.DataFrame  (one row per region)
        Required columns:
            'region_id' (INDEX): identifier for region (must be unique to each region)
            'geometry' (shapely.wkt/geom.wkt):  Multi-polygon representing regions location and shape.

    actuals: list of actual site values as pandas.DataFrame (one row per timestamp/site_id combination)
        Required columns:
            'timestamp' (string): timestamp of actual reading
            'site_id': ID of site which took actual reading (must match with a sites.site_id
                in sites (in value and type))
            [one or more value columns] (float):    value of actual measurement readings.
                                                    each column name should be the name of the measurement e.g. 'NO2'
            verbose: (int) Verbosity of output level. zero or less => No debug output
    
    Returns:
                Initialised instance of subclass of RegionEstimator


	'''

estimator = RegionEstimatorFactory.region_estimator(method_name, df_sites, df_regions, df_actuals)


# Call RegionEstimator.get_estimations
# Required inputs:
# 	region_id:      region identifier (string (or None to get all regions))
# 	timestamp:      timestamp identifier (string (or None to get all timestamps))
#   print_progress  print progress (boolean, default:False)
#
#	WARNING! - estimator.get_estimates(None, None) will calculate every region at every timestamp.


result = estimator.get_estimations('urtica', 'AB', '2018-08-15')

# result is a pandas dataframe, with columns:
#                'measurement'
#                'region_id'
#                'timestamp'
#                'value'  (the estimated value)
#                'extra_data' (extra info about estimation calculation)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://opensource.org/licenses/MIT)
