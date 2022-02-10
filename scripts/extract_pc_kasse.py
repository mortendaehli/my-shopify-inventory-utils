import logging
import os
import urllib.parse
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

import myshopify

logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | [%(pathname)s:%(lineno)d] | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # env_path = Path('.env')
    # load_dotenv(dotenv_path=env_path)
    load_dotenv()

    driver = "ODBC Driver 17 for SQL Server"
    server = os.getenv("SQL_HOST")
    port = os.getenv("SQL_PORT")
    database = "PCKasse"
    username = os.getenv("SQL_USERNAME")
    password = os.getenv("SQL_PASSWORD")

    quoted = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    )

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted), echo=True)

    with open(Path(myshopify.__file__).parent.parent / "db" / "shopify_products.sql", "r") as query_file:
        query = query_file.read()

    df = pd.read_sql(query, con=engine)

    df.to_pickle(Path(myshopify.__file__).parent.parent / "data" / "shopify_products_export.pickle")
