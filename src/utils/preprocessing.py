""" 
"""
import csv
from collections import defaultdict

def get_csv_reader(filepath: str, headers: bool) -> csv.DictReader:
    csv_file = open(filepath, 'r', newline='\n')
    csv_reader = csv.reader(csv_file)
    if headers:
        next(csv_reader)
        return csv_reader
    return csv_reader
    

def extract_fields(filepath: str, indices: list[int]) -> list[list]:
    """ 
    Reads a CSV file. 
    Returns specified fields (columns), defined by indices.
    @param filepath <str>
    @param indices <[int]>
    @returns <[[str, int]]>
    """
    rows_filtered = []
    with open(filepath, 'r', newline='\n') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            row_filtered = []
            for index in indices:
                row_filtered.append(row[index])
            rows_filtered.append(row_filtered)
    return rows_filtered

def transform_fields_integer(rows: list[list], indices: list[int]) -> list[list]:
    """ 
    Returns rows containing corrected fields transformed into integers.
    """
    rows_transformed = []
    field_number = len(rows[0])
    # determine which indices are not transformed
    indices_others = list(range(field_number))
    for index in indices: indices_others.remove(index)
    # loop through rows
    for row in rows:
        row_transformed = [0]*field_number
        # other indices remain unchanged
        for index in indices_others: 
            row_transformed[index] = row[index]
        # transform to int
        for index in indices:
            row_transformed[index] = int(row[index])
        rows_transformed.append(row_transformed)
    return rows_transformed

def filter_empty_strings(rows: list[list], indices: list[int]) -> list[list]:
    """
    Returns a curated list of rows without empty strings
    """
    filtered_rows = []
    for row in rows:
        for index in indices:
            row[index] = row[index].strip()
        if all(row[index] != "" for index in indices):
            filtered_rows.append(row)
    return filtered_rows

def filter_fields_strings_duplicates(rows: list[list], index: int) -> list[list]:
    """
    Returns curated list of rows without duplicates
    """
    company_dict = defaultdict(list)
    row_len = len(rows[0])
    
    row_cached = None
    row_new = None

    # fill dictionary of unique company entries
    for row in rows:
        if row[index] not in company_dict:
            company_dict[row[index]] = row
        else:
            # define rows to be merged
            row_cached = company_dict[row[index]]
            row_new = [0]*row_len
            
            for i in range(row_len):
                # when non-summable index
                if i == index: row_new[i] = row[index]
                # merge corresponding entries
                else: row_new[i] = row[i] + row_cached[i]
            
            # replace old entry in DICT
            company_dict[row[index]] = row_new
    
    # loop through dictionary and return list
    return list(company_dict.values())

def filter_empty_fields(rows: list[list]) -> list[list]:
    """
    """
    filtered_rows = []
    row_len = len(rows[0])
    for row in rows:
        if all(row[index] != None for index in range(row_len)):
            filtered_rows.append(row)
    return filtered_rows

def format_fields_string_wrapper(rows: list[list], indices: list[int]) -> list[list]:
    """
    Returns a curated list of rows with strings envolved by " "
    """
    for row in rows:
        for index in indices:
            row[index] = '"' + row[index] + '"'
    return rows

def combine_fields_sum(rows: list[list], indices: list[list[int]]) -> list[list]:
    """
    Returns reduced mapping of fields (some columns need to be combined into an aggregate)
    """
    rows_combined_fields = []
    for row in rows:
        row_new = [row[0]]
        for cidx in indices:
            new_field = sum([row[idx] for idx in cidx])
            row_new.append(new_field)
        rows_combined_fields.append(row_new)
    return rows_combined_fields