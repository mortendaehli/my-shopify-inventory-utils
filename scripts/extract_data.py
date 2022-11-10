import logging
import urllib.parse
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

from myshopify.config import config

logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "data"
SQL_SCRIPT_PATH = Path(__file__).parent / "sql"

if __name__ == "__main__":
    # docker-compose run --rm backend python scripts/extract_data.py
    sql_driver = "ODBC Driver 17 for SQL Server"
    sql_server = config.SQL_HOST
    sql_port = config.SQL_PORT
    sql_database = "PCKasse"
    sql_username = config.SQL_USERNAME
    sql_password = config.SQL_PASSWORD

    print("*** Extracting data from database")
    with open(SQL_SCRIPT_PATH / "shopify_products.sql", "r") as query_file:
        extract_query = query_file.read()
    quoted = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_server};DATABASE={sql_database};UID={sql_username};PWD={sql_password}"
    )

    engine = create_engine(
        "mssql+pyodbc:///?odbc_connect={}".format(quoted), echo=True, connect_args={"autocommit": True}
    )
    df = pd.read_sql(extract_query, con=engine)

    df.to_pickle(str(DATA_PATH / "shopify_products_export.pickle"))
