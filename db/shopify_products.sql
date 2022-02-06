WITH Products AS (
    SELECT
        -- Product
        --art.Description AS body_html,
        --art.Picture AS images,
        web1.Name                                            AS product_type,
        art.Name                                             AS title,
        CASE
            WHEN LOWER(art.Name) LIKE '%janome%' THEN 'Janome'
            WHEN LOWER(art.Name) LIKE '%baby lock%' THEN 'Baby Lock'
            WHEN LOWER(art.Name) LIKE '%brother%' THEN 'Brother'
            ELSE sup.Name
            END                                              AS vendor,

        -- ProductVariant
        art.ArticleNo                                        AS sku,
        art.SalesPrice                                       AS price,

        -- Additional
        art.PriceUnit                                        as price_unit,
        art.HideWebifEmpty                                   AS hide_when_empty,
        CASE WHEN art.OfferPrice > 0 THEN art.OfferPrice END AS discounted_price,
        art.StartOfferPrice                                  AS discount_start,
        art.StopOfferPrice                                   AS discount_end,
        grp.Name AS product_group_name,
        web1.Name AS web_group_name_1,
        web2.Name AS web_group_name_2,
        web3.Name AS web_group_name_3

    FROM Articles art
             LEFT JOIN WebArticleGroup1s web1 ON web1.WebArticleGroup1ID = art.WebArticleGroup1ID
             LEFT JOIN WebArticleGroup2s web2 ON web2.WebArticleGroup2ID = art.WebArticleGroup2ID
             LEFT JOIN WebArticleGroup3s web3 ON web3.WebArticleGroup3ID = art.WebArticleGroup3ID
             LEFT JOIN MainGroups grp ON grp.MainGroupID = art.MainGroupID
             LEFT JOIN Suppliers sup ON sup.SupplierID = art.SupplierID
             LEFT JOIN Manufacturers man ON man.ManufacturerID = art.ManufacturerID
    WHERE art.VisibleOnWeb = 1 -- AND art.MainGroupID = 12
)
SELECT
       product_type,
       title,
       vendor,
       sku,
       price,
       price_unit,
       hide_when_empty,
       CASE WHEN
           CURRENT_TIMESTAMP < discount_end THEN discounted_price END AS discounted_price,
       discount_start,
       discount_end,
       product_group_name,
       web_group_name_1,
       web_group_name_2,
       web_group_name_3,
       CONCAT(product_group_name, ',', web_group_name_1, ',', web_group_name_2, ',', web_group_name_3)    AS tags
FROM Products
;