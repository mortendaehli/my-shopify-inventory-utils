FROM python:3.9 as dev

ARG INSTALL_DEV=true
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install --no-install-recommends -y  unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc && \
  apt-get install --reinstall build-essential -y

RUN echo "[FreeTDS]\n\
Description = FreeTDS Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

RUN pip install poetry && poetry config virtualenvs.create false

WORKDIR /code

COPY /pyproject.toml /poetry.lock ./

RUN bash -c "if [ INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"


RUN pip install pyodbc
