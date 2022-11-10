import logging
import os
import shutil
from datetime import datetime
from ftplib import FTP, error_perm
from logging.handlers import RotatingFileHandler
from pathlib import Path

from myshopify.config import config

logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent / "data"

if __name__ == "__main__":
    if not DATA_PATH.is_dir():
        os.mkdir(DATA_PATH)

    ftp_host = config.FTP_HOST
    ftp_port = config.FTP_PORT
    ftp_user = config.FTP_USERNAME
    ftp_passwd = config.FTP_PASSWORD

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
        timestamp = datetime.strptime(" ".join(col[:2]), "%m-%d-%y %H:%M%p")

        datelist.append(timestamp)
        filelist.append(col[3])

    timestamp, filename = sorted(list(zip(datelist, filelist)), key=lambda x: x[0])[-1]
    print(f"Downloading {filename} timestamp: {timestamp}")
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

    os.remove(DATA_PATH / filename)
    shutil.move(DATA_PATH / str(filename.split(".")[0] + ".bak"), DATA_PATH / "sql.bak")
