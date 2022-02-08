WITH Products AS (
    SELECT
        -- Product
        art.Description AS body_html,
        art.Picture AS images,
        ISNULL(web1.Name, 'Annet') AS product_type,
        art.Name                                             AS title,
        CASE
            WHEN art.Name LIKE '%janome%' THEN 'Janome'
            WHEN REPLACE(art.Name, ' ', '')  LIKE '%baby lock%' THEN 'Baby Lock'
            WHEN art.Name LIKE '%brother%' THEN 'Brother'
            WHEN sup.Name LIKE 'byannie' THEN 'By Annie'
            WHEN sup.Name LIKE 'annaka' THEN 'AnnAKa'
            ELSE sup.Name
            END                                              AS vendor,

        -- ProductVariant
        art.ArticleNo                                        AS sku,
        CASE
            WHEN grp.MainGroupID = 10 THEN art.SalesPrice
            ELSE CAST(art.SalesPrice AS FLOAT) * 1.25
            END AS price,

        -- Additional
        art.ArticleID AS PCKasseID,
        art.PriceUnit                                        AS price_unit,
        CASE
            WHEN grp.Name LIKE 'symaskiner' THEN 0
            ELSE 1
            END                                   AS hide_when_empty,
        CASE WHEN art.OfferPrice > 0 THEN art.OfferPrice END AS discounted_price,
        art.StartOfferPrice                                  AS discount_start,
        art.StopOfferPrice                                   AS discount_end,
        CASE
            WHEN grp.Name LIKE 'Quilting Supplies & Scissors' THEN N'Quilte-tilbehør'
            WHEN grp.Name LIKE 'Trim, Gifts, & Specialties' THEN 'Gaver'
            ELSE grp.Name
            END AS product_group_name,
        CASE
            WHEN web1.Name LIKE 'Quiltestoffer' THEN 'Quilte-stoff'
            WHEN web1.Name LIKE 'ikke i bruk' THEN NULL
            ELSE web1.Name
            END AS web_group_name_1,
        CASE
            WHEN web2.Name LIKE 'Norske design' THEN 'Norsk design'
            WHEN web2.Name LIKE 'Linjaler' THEN 'Linjal'
            WHEN web2.Name LIKE 'Utenlandske design' THEN 'Internasjonalt design'
            WHEN web2.Name LIKE 'ikke i bruk' THEN NULL
            ELSE web2.Name
            END AS web_group_name_2,
        CASE
            WHEN web3.Name LIKE 'Diverse designere' THEN NULL
            WHEN web3.Name LIKE 'ikke i bruk' THEN NULL
            ELSE web3.Name
            END AS web_group_name_3,
        CASE WHEN CAST(CURRENT_TIMESTAMP - LastUpdate AS INT) < 90 THEN 'Nyhet' END AS new_tag

    FROM Articles art
             LEFT JOIN WebArticleGroup1s web1 ON web1.WebArticleGroup1ID = art.WebArticleGroup1ID
             LEFT JOIN WebArticleGroup2s web2 ON web2.WebArticleGroup2ID = art.WebArticleGroup2ID
             LEFT JOIN WebArticleGroup3s web3 ON web3.WebArticleGroup3ID = art.WebArticleGroup3ID
             LEFT JOIN MainGroups grp ON grp.MainGroupID = art.MainGroupID
             LEFT JOIN Suppliers sup ON sup.SupplierID = art.SupplierID
             LEFT JOIN Manufacturers man ON man.ManufacturerID = art.ManufacturerID
    WHERE art.VisibleOnWeb = 1
)
SELECT
       CASE
           WHEN price_unit LIKE 'meter' THEN CONCAT('Pris per desimeter' + CHAR(10) + CHAR(10), body_html)
           ELSE body_html
           END AS body_html,
       images,
       product_type,
       title,
       vendor,
       PCKasseID,  -- remove me.
       pro.sku,
       CASE
            WHEN price_unit LIKE 'meter' THEN ROUND(CAST(price AS FLOAT) * 10.0, 1)  -- This is stupid! meter is in fact cm.
            WHEN price IS NULL THEN 0
            ELSE price
            END AS price,
       price AS org_price,
       CASE
            WHEN price_unit LIKE 'meter' THEN 'desimeter'
            ELSE price_unit
            END AS price_unit,
       CASE
            WHEN price_unit LIKE 'meter' THEN (CAST(rec.C AS FLOAT) - CAST(sol.C AS FLOAT)) / 10.0  -- This is stupid! meter is in fact cm.
            ELSE rec.C - sol.C
            END AS available,
       hide_when_empty,
       CASE WHEN
           CURRENT_TIMESTAMP < discount_end THEN discounted_price END AS discounted_price,
       discount_start,
       discount_end,
       product_group_name,
       web_group_name_1,
       web_group_name_2,
       web_group_name_3,
       CONCAT(product_group_name, ',', web_group_name_1, ',', web_group_name_2, ',', web_group_name_3, ',', new_tag)    AS tags
FROM Products pro
LEFT JOIN Sold sol ON sol.aid = pro.PCKasseID
LEFT JOIN Received rec ON rec.aid = pro.PCKasseID AND (rec.C > 0 OR pro.images IS NOT NULL)
--ORDER BY pro.sku
;