import logging
import os
import shutil
from datetime import datetime
from ftplib import FTP, error_perm
import urllib.parse
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd
import time


logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "data"
SQL_SCRIPT_PATH = Path(__file__).parent / "sql"

if __name__ == "__main__":
    if not DATA_PATH.is_dir():
        os.mkdir(DATA_PATH)

    ftp_host = os.getenv("FTP_HOST")
    ftp_port = os.getenv("FTP_PORT")
    ftp_user = os.getenv("FTP_USERNAME")
    ftp_passwd = os.getenv("FTP_PASSWORD")

    sql_driver = "ODBC Driver 17 for SQL Server"
    sql_server = os.getenv("SQL_HOST")
    sql_port = os.getenv("SQL_PORT")
    sql_database = "PCKasse"
    sql_username = os.getenv("SQL_USERNAME")
    sql_password = os.getenv("SQL_PASSWORD")

    ftp = FTP()
    ftp.connect(host=ftp_host, port=int(ftp_port))
    ftp.login(user=ftp_user, passwd=ftp_passwd)
    ftp.cwd("/")

    data = list()
    ftp.dir(data.append)
    datelist = list()
    filelist = list()
    for line in data:
        col = line.split()
        datestr = " ".join(line.split()[5:8])
        try:
            timestamp = datetime.strptime(datestr, "%b %d %Y")
        except ValueError:
            timestamp = datetime.strptime(datestr + " " + str(datetime.now().year), "%b %d %H:%M %Y")

        datelist.append(timestamp)
        filelist.append(col[8])

    timestamp, filename = sorted(list(zip(datelist, filelist)), key=lambda x: x[0])[-1]
    print(f"Downloading {filename}")
    try:
        ftp.retrbinary("RETR %s" % filename, open(DATA_PATH / filename, "wb").write)
    except error_perm:
        print("Error: cannot read file %s" % filename)
        os.unlink(filename)
    else:
        print("***Downloaded*** %s " % filename)

    ftp.quit()

    print("***Extracting*** %s " % filename)

    shutil.unpack_archive(DATA_PATH / filename, extract_dir=DATA_PATH)
    os.remove(os.remove(DATA_PATH / filename))
    shutil.move(DATA_PATH / str(filename.split(".")[0] + ".bak"), DATA_PATH / "sql" / "sql.bak")

    print("*** Restoring database from backup")
    with open(SQL_SCRIPT_PATH / "restore.sql", "r") as query_file:
        restore_query = query_file.read()

    quoted_master = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_server};DATABASE=master;UID={sql_username};PWD={sql_password}"
    )

    engine_master = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted_master), echo=True)
    engine_master.execute(restore_query)
    time.sleep(30)

    print("*** Extracting data from database")
    with open(SQL_SCRIPT_PATH / "shopify_products.sql", "r") as query_file:
        extract_query = query_file.read()
    quoted = urllib.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={sql_server};DATABASE={sql_database};UID={sql_username};PWD={sql_password}"
    )

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(quoted), echo=True)
    df = pd.read_sql(extract_query, con=engine)

    df.to_pickle(str(DATA_PATH / "shopify_products_export.pickle"))
