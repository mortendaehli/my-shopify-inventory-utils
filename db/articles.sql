SELECT TOP(100)
    art.ArticleID AS ID,  -- POS ID
    art.ArticleNo AS SKU,
    art.Name AS Title,
    art.SalesPrice,
    art.PurchasePrice,
    art.PriceUnit,
    art.PriceUnitAmount,
    uni.Name AS UnitName,
    sup.Name AS SupplierName,
    man.Name AS ManufacturerName,
    art.SupplierARticleNo AS SupplierArticleNo,
    ean.EanNo AS EAN,
    art.OfferPrice AS DiscountedPrice,
    art.StartOfferPrice AS DiscountStart,
    art.StopOfferPrice AS DiscountEnd,
    art.Description AS Description,
    art.VisibleOnWeb AS IsActive,
    art.HideWebifEmpty AS HideWhenEmpty,
    art.Picture AS ProductImage,
    art.MainGroupID AS MainProductGroupID,
    grp.Name AS MainProductGroupName,
    art.WebArticleGroup1ID AS ProductGroup1ID,
    art.WebArticleGroup2ID AS ProductGroup2ID,
    art.WebArticleGroup3ID AS ProductGroup3ID,
    web1.Name AS ProductGroupName1,
    web2.Name AS ProductGroupName2,
    web3.Name AS ProductGroupName3

FROM Articles art
LEFT JOIN MainGroups grp ON grp.MainGroupID = art.MainGroupID
LEFT JOIN WebArticleGroup1s web1 ON web1.WebArticleGroup1ID = art.WebArticleGroup1ID
LEFT JOIN WebArticleGroup2s web2 ON web2.WebArticleGroup2ID = art.WebArticleGroup2ID
LEFT JOIN WebArticleGroup3s web3 ON web3.WebArticleGroup3ID = art.WebArticleGroup3ID
LEFT JOIN Units uni ON uni.UnitID = art.UnitID
LEFT JOIN Suppliers sup ON sup.SupplierID = art.SupplierID
LEFT JOIN Manufacturers man ON man.ManufacturerID = art.ManufacturerID
LEFT JOIN EanNos ean ON ean.ArticleID = art.ArticleId
WHERE art.MainGroupID = 12 AND ArticleNo LIKE 48344
;

SELECT com.MainArticleID AS component_id, art.ArticleID, art.Name, art.PriceUnit, art.SalesPrice AS price_unit, art.Name2
    FROM Articles art
             LEFT JOIN WebArticleGroup1s web1 ON web1.WebArticleGroup1ID = art.WebArticleGroup1ID
             LEFT JOIN WebArticleGroup2s web2 ON web2.WebArticleGroup2ID = art.WebArticleGroup2ID
             LEFT JOIN WebArticleGroup3s web3 ON web3.WebArticleGroup3ID = art.WebArticleGroup3ID
             LEFT JOIN MainGroups grp ON grp.MainGroupID = art.MainGroupID
             LEFT JOIN Suppliers sup ON sup.SupplierID = art.SupplierID
             LEFT JOIN Manufacturers man ON man.ManufacturerID = art.ManufacturerID
             LEFT JOIN Sold sol ON sol.aid = art.ArticleID
             LEFT JOIN Received rec ON rec.aid = art.ArticleID AND (rec.C > 0 OR art.Picture IS NOT NULL)
             LEFT JOIN Components com on art.ArticleID = com.ArticleID
WHERE art.ArticleID >= 56235 AND art.Name2 IS NOT NULL


SELECT * FROM Articles WHERE ArticleNo = '105066'