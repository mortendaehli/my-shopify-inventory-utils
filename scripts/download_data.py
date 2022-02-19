import logging
import os
from datetime import datetime
from ftplib import FTP, error_perm
from logging.handlers import RotatingFileHandler
from pathlib import Path
import shutil
import myshopify

from dotenv import load_dotenv

logging_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
file_handler = RotatingFileHandler(Path(__file__).parent / ".log", maxBytes=1000, backupCount=0)
stream_handler = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, stream_handler], format=logging_format)

logger = logging.getLogger(__name__)

DATA_PATH = Path(myshopify.__file__).parent.parent / "data" / "db"

if __name__ == "__main__":
    if not DATA_PATH.is_dir():
        os.mkdir(DATA_PATH)

    load_dotenv()
    host = os.getenv("FTP_HOST")
    port = os.getenv("FTP_PORT")
    user = os.getenv("FTP_USERNAME")
    passwd = os.getenv("FTP_PASSWORD")

    ftp = FTP()
    ftp.connect(host=host, port=int(port))
    ftp.login(user=user, passwd=passwd)
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

    shutil.unpack_archive(DATA_PATH / filename, extract_dir=DATA_PATH)
