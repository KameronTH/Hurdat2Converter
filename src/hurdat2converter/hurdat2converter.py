import geopandas as gpd
import pandas as pd
import logging
import os
from typing import Union

class UnexpectedRowSize(Exception):
    """This exception will be raised if a row with an unexpected length is given."""
    pass

def parse_hurdat2(file_name: str | os.PathLike) -> tuple[list, list]:
    """This function takes the raw HURDATA2 csv files and converts the data into lists. The header_rows list contains information to identify the hurricane.The data_rows list contains information that corresponds to the identified hurricane. Both lists can be joined using the hurricane id value."""
    header_rows = [] # Contains Hurrican identification like name and ID.
    data_rows = [] # Contains weather and geographic data for a particular hurricane.

    with open(file_name, "r") as f:
        raw_lines = f.readlines()
        logging.info(f"Opened file, {file_name} in read mode. File should be HURDAT2 data.")
    remove_break = [x.replace("\n", "") for x in raw_lines]
    logging.info(f"Read the data into list using line breaks.")

    split_rows = [x.split(",") for x in remove_break]
    logging.info(f"Columns were split based on ',' since data is in a csv format.")
    for row in split_rows:
        if row[-1] == "":
            row = row[:-1]
        else:
            pass

        row = [x.strip(" ") for x in row] # Removed empty spaces on ends of data

        # The headers rows are on new lines along with data rows, this if statement separates the header row, which contains hurricane identification information and assigns it to the header_rows list. Every row after this is a data row until a new header row is present. This is why the header row is identified when len(row) == 3, instead of being calculated outside the if statement.

        if len(row) == 3: # Some rows contain header data
            header_rows.append(row)
            logging.info("Added header rows into a list.")
            HURRICANE_ID = row[0]

        elif len(row) == 21:
            data_rows.append(row + [HURRICANE_ID])
            logging.info("Added data rows into a list.")
        else:
            raise UnexpectedRowSize(f"A row with an unexpected size was found. The row was size {len(split_rows)}, but should only be 4 columns if a header row or 21 columns if a data row. The last row for header data should be empty")

    return header_rows, data_rows

def create_dataframe_for_headers_rows(header_data:list) -> pd.DataFrame:
    """This function creates a dataframe from the hurricane identification information. The column names were created by the scriptwriter and based on the data's metadata"""
    header_data = pd.DataFrame(header_data, columns=["Hurricane_ID", "Hurricane_Name", "Number_recorded"])  # These names were custom-made by scriptwriter.
    return header_data

def _convert_lat_coords(lat_NS:str) -> float:
    """A helper function for converting latitude values into floats."""
    if lat_NS[-1] == "N":
        lat_conversion = float(lat_NS[:-1])
    elif lat_NS[-1] == "S":
        lat_conversion = -float(lat_NS[:-1])
    else:
        raise ValueError(f"The provided latitude should be N or S, not {lat_NS[:-1]}.")
    return lat_conversion

def _convert_long_coords(long_WE:str) -> float:
    """A helper function for converting longitude values into floats."""

    if long_WE[-1] == "E":
        long_conversion = float(long_WE[:-1])
    elif long_WE[-1] == "W":
        long_conversion = -float(long_WE[:-1])
    else:
        raise ValueError(f"The provided latitude should be E or W, not {long_WE[:-1]}.")
    return long_conversion


def create_geodataframe_for_data_rows(row_data:list) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """This function converts the rows containing hurricane data into geodataframes. The first return is a geodataframe representation of data processed with by the scriptwriter using the availible documentation. The secondd return is a geodataframe representation of the raw data."""
    # TODO: Check that data has correct number of columns.
    columns = ["date",
               "time",
               "record_identifier",
               "system_status",
               "latitude",
               "longitude",
               "maximum_sustained_wind_kt",
               "minimum_pressure_mb",
               "34_kt_wind_radii_maximum_extent_in_northeastern_quadrant_NM",
               "34_kt_wind_radii_maximum_extent_in_southeastern_quadrant_NM",
               "34_kt_wind_radii_maximum_extent_in_southwestern_quadrant_NM",
               "34_kt_wind_radii_maximum_extent_in_northwestern_quadrant_NM",
               "50_kt_wind_radii_maximum_extent_in_northeastern quadrant_NM",
               "50 kt wind radii maximum extent in southeastern quadrant_NM",
               "50 kt wind radii maximum extent in southwestern quadrant_NM",
               "50 kt wind radii maximum extent in northwestern quadrant_NM",
               "64 kt wind radii maximum extent in northeastern quadrant_NM",
               "64 kt wind radii maximum extent in southeastern quadrant_NM",
               "64 kt wind radii maximum extent in southwestern quadrant_NM",
               "64 kt wind radii maximum extent in northwestern quadrant_NM",
               "radius_of_maximum_wind_NM",
               "Hurricane_ID"]

    columns = [x.replace(" ", "_") for x in columns]
    pre_processed_geodataframe = gpd.GeoDataFrame(row_data, columns=columns)
    post_processed_geodataframe = pre_processed_geodataframe.copy()

    # Using appy to make two arrays which contain the converted lat and long coordinates so that geodataframe can have geometry.
    post_processed_geodataframe = post_processed_geodataframe.set_geometry(gpd.points_from_xy(post_processed_geodataframe["longitude"].apply(_convert_long_coords), post_processed_geodataframe["latitude"].apply(_convert_lat_coords), crs=4326))
    post_processed_geodataframe.loc[:, "date"] = pd.to_datetime(post_processed_geodataframe["date"], format="%Y%m%d").dt.date

    post_processed_geodataframe.loc[:, "time"] = post_processed_geodataframe["time"].apply(lambda x: f"{x[0:2]}:{x[2:4]}")
    post_processed_geodataframe.loc[:, "time"] = pd.to_datetime(post_processed_geodataframe['time'],format='%H:%M').dt.time

    post_processed_geodataframe.loc[:, "datetime"] = pd.to_datetime(post_processed_geodataframe["date"].astype(str) + " " + post_processed_geodataframe['time'].astype("str"), format="%Y-%m-%d %H:%M:%S")
    post_processed_geodataframe = post_processed_geodataframe.drop(columns=["date", "time"]) # Drops columns in favor of one datetime columns.
    return post_processed_geodataframe, pre_processed_geodataframe

def join_hurricane_data(header: pd.DataFrame, data: Union[pd.DataFrame | gpd.GeoDataFrame]) -> gpd.GeoDataFrame | pd.DataFrame:
    """This function joins the dataset containing hurricane identification information and weather data using the Hurricane_ID field."""
    #TODO: Make sure columns for each dataset are the expected number
    if type(header) is pd.DataFrame and header.shape[1] == 3:
        joined_datasets = data.merge(header, on="Hurricane_ID", how="left")
    else:
        raise TypeError("The data provided for the header parameter should be a pandas dataframe with 3 columns.")
    return joined_datasets