# Adventure Works Database on SQL Server 2019
FROM mcr.microsoft.com/mssql/server:2019-latest@sha256:a098c9ff6fbb8e1c9608ad7511fa42dba8d22e0d50b48302761717840ccc26af

ARG MSSQL_SA_PASSWORD
ARG ACCEPT_EULA=Y

USER root
RUN mkdir /data
COPY data/sql.bak /data/sql.bak

# RUN chown -R mssql /data
# RUN chown -R mssql /var/opt/mssql
# USER mssql

# RUN (/opt/mssql/bin/sqlservr --accept-eula & ) | grep -q "Starting database restore" \
#     && /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P ${MSSQL_SA_PASSWORD} -i /src/restore.sql
# -d master
# RUN rm /src/sql.bak && rm /src/restore.sql
