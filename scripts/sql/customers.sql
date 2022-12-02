-- Do we need to export customers?
SELECT
    Name as Name,
    MailingAddress AS Address,
    MailingCity As Location,
    'Norway' AS Country,
    SUBSTRING(MailingZip, 0, 5) AS Zip,
    Telephone AS PhoneNumber,
    Email AS EmailAddress,
    IIF(CompanyNo LIKE '' OR CompanyNo is NULL, 'Privat', 'Bedrift') AS CustomerGroup,
    1 AS SyncToSmW,
    1 AS Department

FROM Customers;

SELECT TOP(100) * FROM Customers;