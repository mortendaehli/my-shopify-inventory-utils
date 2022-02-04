# Ubuntu 20.04 base with Python runtime and pyodbc to connect to SQL Server
FROM ubuntu:20.04

WORKDIR /code

# apt-get and system utilities
RUN apt-get update && apt-get install -y \
    curl apt-utils apt-transport-https debconf-utils gcc build-essential g++\
    && rm -rf /var/lib/apt/lists/*

# adding custom Microsoft repository
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install SQL Server drivers
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

# install SQL Server tools
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN /bin/bash -c "source ~/.bashrc"

# python libraries
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# install necessary locales, this prevents any locale errors related to Microsoft packages
RUN apt-get update && apt-get install -y locales \
    && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
    && locale-gen

# you can also use regular install of the packages
RUN pip3 install pyodbc SQLAlchemy ShopifyAPI python-dotenv pandas Pillow pydantic retry
