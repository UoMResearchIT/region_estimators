# region_estimators package

region_estimators is a Python library to calculate regional estimations of scalar quantities, based on some known scalar quantities at specific locations.
For example, estimating the NO2 (pollution) level of a postcode/zip region, based on sensor data nearby.  
This first version of the package is initialised with 2 estimation methods: 
1. Diffusion: look for actual data points in gradually wider rings, starting with sensors within the region, and then working in rings outwards, until sensors are found. If more than one sensor is found at the final stage, it takes the mean.
2. Simple Distance measure: This is a very basic implementation... Find the nearest sensor to the region and use that value. 
If sensors exist within the region, take one of those. (Todo: If multiple sensors exist within the region -take the mean)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install region_estimators.

```bash
pip install region_estimators
```

## Usage

```python
import region_estimators

# Call RegionEstimatorFactory.region_estimator
# Reguired inputs: 
# 	method_name (string): the estimation method. For example, in the first version the options are 'diffusion' or 'distance-simple'


# 	3 pandas.Dataframe objects:

	'''
	sensors: list of sensors as pandas.DataFrame (one row per sensor)
	    Required columns:
                'sensor_id' (integer): identifier for sensor (must be unique to each sensor)
                'latitude' (float): latitude of sensor location
                'longitude' (float): longitude of sensor location

        regions: list of regions as pandas.DataFrame  (one row per region)
            Required columns:
                'region_id' (string): identifier for region (must be unique to each region)
                'geom' (shapely.wkt/geom.wkt):  Multi-polygon representing regions location and shape.

        actuals: list of sensor values as pandas.DataFrame (one row per timestamp)
            Required columns:
                'timestamp' (string): timestamp of actual reading
                'sensor' (integer): ID of sensor which took actual reading (must match sensors.sensor_id above)
                'value' (float): scalar value of actual reading
	'''

estimator = RegionEstimatorFactory.region_estimator(method_name, df_sensors, df_regions, df_actuals)

# region_id:  region identifier (string (or None to get all regions))
# timestamp:  timestamp identifier (string (or None to get all timestamps))

result = estimator.get_estimations(region_id, timestamp)

# result is json list of dicts, each with
#                i) 'region_id'
#                ii) calculated 'estimates' (list of dicts, each containing 'value', 'extra_data', 'timestamp')


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://opensource.org/licenses/MIT)