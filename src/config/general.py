import os

# INPUT and OUTPUT CSV FILEPATHS
CSV_INPUT_PATH = "../../data/input/h1b_datahubexport-2022.csv"
CSV_OUTPUT_PATH = "../../data/output/h1b_datahubexport-2022.csv"

# DB CREDENTIALS
DB_USER = os.environ.get('AWS_RDS_VISASPOTTER_USER')
DB_PASSWORD = os.environ.get('AWS_RDS_VISASPOTTER_PASSWORD')
DB_HOSTNAME = os.environ.get('AWS_RDS_VISASPOTTER_HOSTNAME')
DB_DBNAME = os.environ.get('AWS_RDS_VISASPOTTER_DBNAME')