from src.hurdat2converter import hurdat2converter
from unittest import TestCase, main
from pprint import pprint

hurdat2_atlantic_file = "../data/Atlantic_hurricane_database_(HURDAT2)_hurdat2-1851-2023-051124.csv"
hurdat2_ne_nc = "../data/Northeast_and_North_Central_Pacific_hurricane_database_hurdat2-nepac-1949-2023-042624.csv"

class Converter(TestCase):
    def setUp(self):
        self.hurricane_atlantic_header, self.hurricane_atlantic_data = hurdat2converter.parse_hurdat2(hurdat2_atlantic_file)
        self.hurricane_ne_nc_header, self.hurricane_ne_nc_data = hurdat2converter.parse_hurdat2(hurdat2_ne_nc)

    def test_hurricane_info_list(self):
        pprint(self.hurricane_atlantic_header[0:5])

    def test_specific_hurricane_data(self):
        pprint(self.hurricane_atlantic_data[0:5])

    def test_create_dataframe_for_headers_rows(self):
        df = hurdat2converter.create_dataframe_for_headers_rows(self.hurricane_atlantic_header)
        print(df.head())

    def test_create_geodataframe_for_data_rows(self):
        post_process_gdf, pre_process_df = hurdat2converter.create_geodataframe_for_data_rows(self.hurricane_atlantic_data)
        print(post_process_gdf.head())
        print(pre_process_df.head())

    def test_join_hurricane_data(self):
        post_process_gdf, pre_process_df = hurdat2converter.create_geodataframe_for_data_rows(self.hurricane_atlantic_data)
        header_df = hurdat2converter.create_dataframe_for_headers_rows(self.hurricane_atlantic_header)
        preprocessed_hurricane_data = hurdat2converter.join_hurricane_data(header_df, pre_process_df)
        post_processed_hurricane_data = hurdat2converter.join_hurricane_data(header_df, post_process_gdf)

        print(type(preprocessed_hurricane_data))
        print(type(post_processed_hurricane_data))

if __name__ == "__main__":
    main()
