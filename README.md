# hurdat2converter
Converts NOAA's HURDAT2 Data to a more readable format.
# Purpose
The purpose of these modules is to parse data provided by NOAA's National Hurricane Center (NHC) HURDAT2 datasets into a 
more readable and data analysis ready format. The dataset is provided as a single text file containing information on 
the hurricane's identity and additional data about the hurricane.

This project separates those two types of data into separate tables and provides an option to join the two tables as 
pandas dataframes or GeoPandas GeoDataframes. These objects can then be exported to geospatial or tabular files or 
further analyzed.

The HURDAT2 datasets used was last updated April 26th, 2024, and includes hurricane data up to 2023.
# Requirements
## Third Party Packages
Packages installed through Conda\
geopandas Version 0.14.2\
pandas 2.2.2

## Example Usage
```python
from src.hurdat2converter import hurdat2converter
from geopandas import GeoDataFrame
from pandas import DataFrame
hurdat2_atlantic_file = "../data/Atlantic_hurricane_database_(HURDAT2)_hurdat2-1851-2023-051124.csv"

# Parse the data into two lists
atlanta_hurricane_info, atlanta_hurricane_data = hurdat2converter.parse_hurdat2(hurdat2_atlantic_file)

# Create dataframe or geodataframe from list and joins the data on Hurricane id field.
joined_data = hurdat2converter.join_hurricane_data(hurdat2converter.create_dataframe_for_headers_rows(atlanta_hurricane_info), hurdat2converter.create_geodataframe_for_data_rows(atlanta_hurricane_data)[0])

if type(joined_data) is GeoDataFrame:
    joined_data.to_file("../data/hurricane_data.shp")
elif type(joined_data) is DataFrame:
    joined_data.to_excel("../data/hurricane_data.xlsx")
```

# License
Apache License 2.0 (Apache-2.0)

# Disclaimers
Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.

# References
Kelsey Jordahl, Joris Van den Bossche, Martin Fleischmann, Jacob Wasserman, James McBride, Jeffrey Gerard, … François Leblanc. (2020, July 15). geopandas/geopandas: v0.8.1 (Version v0.8.1). Zenodo. http://doi.org/10.5281/zenodo.3946761
Landsea, C. W. and J. L. Franklin, 2013: Atlantic Hurricane Database Uncertainty and Presentation of a New Database Format. Mon. Wea. Rev., 141, 3576-3592. https://www.nhc.noaa.gov/data/
The pandas development team. (2025). pandas-dev/pandas: Pandas (v2.3.0). Zenodo. https://doi.org/10.5281/zenodo.15597513
