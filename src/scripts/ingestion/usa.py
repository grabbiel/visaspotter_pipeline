"""
Description: Ingest new year data into main table ('h1b_records')
"""
# pip package (imports)
import os
import sys

# set import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# local modules: variables (imports)
from config.general import CSV_OUTPUT_PATH
from config.general import DB_PASSWORD
from config.general import DB_USER
from config.general import DB_HOSTNAME
from config.general import DB_DBNAME

# local modules: queries (import)
from config.ingestion import QUERY_H1BRECORDS_SELECT_ALL

# local modules: db functions (import)
from utils.database import get_cursor
from utils.database import set_db_connection
# local modules: csv functions (import)
from utils.preprocessing import get_csv_reader
from utils.preprocessing import transform_fields_integer
# local modules: queries (import)
from utils.database import query_ranking_update
from utils.database import query_h1brecords_new_year_dump





def main(csv_filepath: str, year: int) -> None:
    
    # set db connection + csv reader +  cursors
    conn = set_db_connection(DB_HOSTNAME, 3315, DB_USER, DB_PASSWORD, DB_DBNAME)
    cursor = get_cursor(conn)
    csv_reader = list(get_csv_reader(csv_filepath, False))

    # curate csv
    rows = transform_fields_integer(csv_reader, [1,2])
    
    print("===== [NEW YEAR DUMP]: START ====")
    query_h1brecords_new_year_dump(cursor, rows, year)
    print("===== [NEW YEAR DUMP]: END ====")
    print("===== [RANKING UPDATE]: START ====")
    query_ranking_update(cursor)
    print("===== [RANKING UPDATE]: END ====")

    #end program
    conn.commit()
    cursor.close()
    conn.close()
    return

if __name__ == "__main__":
    main(CSV_OUTPUT_PATH, 2022)
