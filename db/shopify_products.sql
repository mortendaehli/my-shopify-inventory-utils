SELECT TOP(10)
    -- Product
    art.Description AS body_html,
    art.Picture AS images,
    web1.Name AS product_type,
    CONCAT(web1.Name, ',', web2.Name, ',', web3.Name) AS tags,
    art.Name AS title,
    CASE
        WHEN LOWER(art.Name) LIKE '%janome%' THEN 'Janome'
        WHEN LOWER(art.Name) LIKE '%baby lock%' THEN 'Baby Lock'
        WHEN LOWER(art.Name) LIKE '%brother%' THEN 'Brother'
        ELSE ''
        END AS vendor,

    -- ProductVariant
    art.ArticleNo AS sku,
    art.SalesPrice AS price,

    -- Additional
    art.PriceUnit as price_unit,
    art.HideWebifEmpty AS hide_when_empty,
    sup.Name AS supplier_name,
    CASE WHEN art.OfferPrice > 0 THEN art.OfferPrice END AS discounted_price,
    art.StartOfferPrice AS discount_start,
    art.StopOfferPrice AS discount_end

FROM Articles art
LEFT JOIN WebArticleGroup1s web1 ON web1.WebArticleGroup1ID = art.WebArticleGroup1ID
LEFT JOIN WebArticleGroup2s web2 ON web2.WebArticleGroup2ID = art.WebArticleGroup2ID
LEFT JOIN WebArticleGroup3s web3 ON web3.WebArticleGroup3ID = art.WebArticleGroup3ID
LEFT JOIN Suppliers sup ON sup.SupplierID = art.SupplierID
LEFT JOIN Manufacturers man ON man.ManufacturerID = art.ManufacturerID
WHERE art.MainGroupID = 12 AND art.VisibleOnWeb = 1
;