""" 
Description: Curate CSV file.
"""
# pip package (imports)
import os
import sys

# set import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# local modules (imports)

from utils.csv import export_csv
from utils.preprocessing import extract_fields
from utils.preprocessing import filter_empty_fields
from utils.preprocessing import filter_empty_strings
from utils.preprocessing import transform_fields_integer
from utils.preprocessing import format_fields_string_wrapper
from utils.preprocessing import filter_fields_strings_duplicates
from utils.preprocessing import combine_fields_sum

from config.preprocessing import CSV_INDICES_USA
from config.preprocessing import CSV_INDICES_STRING_USA
from config.preprocessing import CSV_INDICES_INTEGER_USA
from config.preprocessing import CSV_INDICES_COMBINE_USA

from config.general import CSV_INPUT_PATH
from config.general import CSV_OUTPUT_PATH


def main(csv_filepath: str) -> None:
    """ 
    Main function docstring 
    """
    # curate CSV table
    fields_extracted = extract_fields(csv_filepath, CSV_INDICES_USA)
    fields_transformed = transform_fields_integer(fields_extracted, CSV_INDICES_INTEGER_USA)
    fields_filtered = filter_empty_strings(fields_transformed, CSV_INDICES_STRING_USA)
    fields_filtered = filter_empty_fields(fields_filtered)
    fields_combination = combine_fields_sum(fields_filtered, CSV_INDICES_COMBINE_USA)
    fields_filtered = filter_fields_strings_duplicates(fields_combination, 0)

    # output to new CSV
    export_csv(fields_filtered, CSV_OUTPUT_PATH)
    return


if __name__ == "__main__":
    main(CSV_INPUT_PATH)

