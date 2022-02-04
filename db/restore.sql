-- Simple restoration of a PCKasse MS SQL Express Server
RESTORE FILELISTONLY FROM DISK = '/data/sql.bak';

RESTORE DATABASE PCKasse FROM DISK = '/data/sql.bak'WITH
    MOVE 'PCK' TO '/var/opt/mssql/data/pck.mdf',
    MOVE 'PCK_log' TO '/var/opt/mssql/data/pck_log.ldf'
;

USE PCKasse;