import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
import urllib.parse
import myshopify
import shopify

from myshopify.shopify.inventory import (
    get_all_shopify_resources,

)
from sqlalchemy import create_engine


logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | [%(pathname)s:%(lineno)d] | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    # env_path = Path('.env')
    # load_dotenv(dotenv_path=env_path)
    load_dotenv()
    key = os.getenv("QUILTEFRYD_SHOPIFY_KEY")
    pwd = os.getenv("QUILTEFRYD_SHOPIFY_PWD")
    name = os.getenv("QUILTEFRYD_SHOPIFY_NAME")

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

    # shop = shopify.Shop.current
    products = get_all_shopify_resources(shopify.Product)
    location = shopify.Location.find_first()

    skus = []
    # Updating existing products (variants)
    for product in products:
        for variant in product.variants:
            skus.append(variant.sku)
            if variant.sku in df["sku"].values:
                print("Stop here!")
    print(df)
    print("stop")
