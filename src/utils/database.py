import os
import csv
import pymysql
from typing import Union


def set_db_connection(host: str, port: int, user: str, password: str, database: str) -> Union[pymysql.connections.Connection, None]:
    conn = None
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database=database
        )
        return conn
    except pymysql.connect.Error as E:
        print(E)
    return conn

def get_cursor(conn: pymysql.connections.Connection) -> pymysql.cursors.Cursor:
    cursor = conn.cursor()
    return cursor


def query_h1brecords_exists_company(cursor: pymysql.cursors.Cursor, company: str) -> bool:
    output = None
    cursor.execute(f'''
    SELECT IF (EXISTS (
        SELECT id FROM test_table 
        WHERE company = "{company}"
    ), 1, 0);
    ''')
    output = cursor.fetchone()
    return bool(output[0])

def query_h1brecords_select_code_by_company(cursor: pymysql.cursors.Cursor, company: str) -> int:
    output = None
    cursor.execute(f'''
    SELECT code FROM test_table WHERE company = "{company}";
    ''')
    output = cursor.fetchone()
    return output[0]

def query_h1brecords_select_max_code(cursor: pymysql.cursors.Cursor) -> int:
    output = None
    cursor.execute(f""" 
    SELECT max(code) FROM test_table;
    """)
    output = cursor.fetchone()
    return output[0]

def query_h1brecords_new_entry(cursor: pymysql.cursors.Cursor, company: str, code: int, requests: int, approvals: int, year: int) -> None:
    cursor.execute(f'''
    INSERT INTO test_table (company, code, requests, approvals, fiscal_year, country) 
    VALUES ("{company}", {code}, {requests}, {approvals}, {year}, 0);
    ''')
    return

def query_h1b_sponsorships_update_record(cursor: pymysql.cursors.Cursor, code: str, requests: int, approvals: int) -> None:
    cursor.execute(f"""
    UPDATE h1b_sponsorships SET requests = requests + {requests}, 
                        approvals = approvals + {approvals} 
    WHERE id = {code};
    """)
    return

def query_h1b_sponsorships_new_entry(cursor: pymysql.cursors.Cursor, code: str, requests: int, approvals: int) -> None:
    cursor.execute(f"""
    INSERT INTO h1b_sponsorships (id, requests, approvals) 
    VALUES ({code}, {requests}, {approvals});
    """)
    return

def query_ranking_update(cursor: pymysql.cursors.Cursor) -> None:
    cursor.execute("CALL UPDATE_RANKINGS();")
    return

def query_h1brecords_new_year_dump(cursor: pymysql.cursors.Cursor, rows: list[list], year: int) -> None:
    
    new_entry = None

    matching_code = None
    max_code = query_h1brecords_select_max_code(cursor)

    for row in rows:

        # company record existed
        if query_h1brecords_exists_company(cursor, row[0]):
            matching_code = query_h1brecords_select_code_by_company(cursor, row[0])
            new_entry = row + [matching_code]
            print(f"[RECORD STATUS: EXISTING] {new_entry}")
            query_h1b_sponsorships_update_record(cursor, matching_code, new_entry[1], new_entry[2])
        
        # no company record found
        else:
            max_code += 1
            new_entry = row + [max_code]
            print(f"[RECORD STATUS: NEW] {new_entry}")
            query_h1b_sponsorships_new_entry(cursor, max_code, new_entry[1], new_entry[2])
        
        # add new year entry
        query_h1brecords_new_entry(cursor, new_entry[0], new_entry[3], new_entry[1], new_entry[2], 
        year)

    return



