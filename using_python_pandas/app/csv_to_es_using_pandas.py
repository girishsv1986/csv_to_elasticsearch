"""
This python module demonstrates how to -
 1. Read data from a csv/excel file using python pandas library
 2. Do data clean up to remove/correct dirty data, bring data into required formats using
    pandas available API.
 3. Push the cleaned data to elastic search instance

This module imports data to elasticsearch instance running on localhost 9200 port
which can be override by setting the environment variable "ES_HOST" and "ES_PORT" value
"""
import pandas as pd
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers


ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_CLIENT = Elasticsearch(f"{ES_HOST}:{ES_PORT}", http_compress=True)

# Inside importer image csv files and py files are copied on same directory
CSV_FILE_PATH = "summer-products-with-rating-and-performance_2020-08.csv"

# name of columns containing 0 and 1 values
BOOLEAN_VALUE_COLUMNS = [
    "badge_local_product",
    "badge_product_quality",
    "badge_fast_shipping",
    "shipping_is_express",
    "has_urgency_banner",
    "merchant_has_profile_picture",
    "uses_ad_boosts",
]

NAN_VALUE_MAP = {
    "urgency_text": "",
    "merchant_profile_picture": "",
    "merchant_info_subtitle": "",
    "origin_country": "Unknown",
    "merchant_name": "Unknown",
    "product_color": "Unknown",
    "product_variation_size_id": "Unknown",
    "rating_one_count": 0,
    "rating_two_count": 0,
    "rating_three_count": 0,
    "rating_four_count": 0,
    "rating_five_count": 0,
}


def perform_data_clean(df):
    """
    Cleans up given data frame for
        1. Replaces not a number values with the values for the columns mentioned in
            NAN_VALUE_MAP constant.
        2. Converts integer 0, 1 values to boolean for columns mentioned in
            BOOLEAN_VALUE_COLUMNS constant.

    Args:
        df (pd.DataFrame): data frame to be cleaned up
    """
    # Perform data cleanup
    for col, value in NAN_VALUE_MAP.items():
        df[col] = df[col].fillna(value)

    for col in BOOLEAN_VALUE_COLUMNS:
        df[col] = df[col].astype("bool")


def docs_generator(df):
    """
    Iterator function to yield json doc for each data frame row in json format as required
        by Elasticsearch bulk API

    Args:
        df (pd.DataFrame): data frame to be cleaned up

    Yield:
        dict with key
            - _index
            - _type
            - _source
    """
    for index, document in df.iterrows():
        yield {
            "_index": f"products_rating_performance_{document['origin_country'].lower()}",
            "_type": "_doc",
            "_source": {key: document[key] for key in document.keys()},
        }


if __name__ == "__main__":
    """
    Entry point to process and import data from csv to elasticsearch  
    """
    print(f"Importing data from {CSV_FILE_PATH} ...")
    df = pd.read_csv(CSV_FILE_PATH)
    perform_data_clean(df)
    helpers.bulk(ES_CLIENT, docs_generator(df))
    print("Imported data successfully...")
