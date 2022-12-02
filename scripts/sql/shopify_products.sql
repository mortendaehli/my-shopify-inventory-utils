WITH Products AS (SELECT
                      -- Product
                      art.Description                                                                                                                                                 AS body_html,
                      art.Picture                                                                                                                                                     AS images,
                      art.Name                                                                                                                                                        AS title,

                      -- ProductVariant
                      art.ArticleID                                                                                                                                                   AS sku,
                      art.ArticleNo AS barcode,
                      art.LastUpdate                                                                                                                                                  AS source_updated,
                      art.PurchasePrice                                                                                                                                               AS purchase_price,
                      IIF(grp.MainGroupID = 10, 0, 25)                                                                                                                                AS vat_rate,
                      IIF(grp.MainGroupID = 10, CAST(art.SalesPrice AS FLOAT), CAST(art.SalesPrice AS FLOAT) * 1.25)                                                                  AS price,
                      LOWER(IIF(art.PriceUnit IS NULL or art.PriceUnit = '', 'stk', art.PriceUnit))                                                                                   AS price_unit,
                      IIF(art.PriceUnit LIKE 'meter%', FLOOR((CAST(ISNULL(rec.C, 0) AS FLOAT) - CAST(ISNULL(sol.C, 0) AS FLOAT)) * 10.0), FLOOR(ISNULL(rec.C, 0) - ISNULL(sol.C, 0))) AS available,
                      IIF(web1.Name LIKE '%symaskin%' OR grp.Name LIKE '%symaskine%', 0, 1)                                                                                           AS hide_when_empty,
                      CASE WHEN art.OfferPrice > 0 THEN IIF(grp.MainGroupID = 10, CAST(art.OfferPrice AS FLOAT), CAST(art.OfferPrice AS FLOAT) * 1.25) END                            AS discounted_price,
                      art.StartOfferPrice                                                                                                                                             AS discount_start,
                      art.StopOfferPrice                                                                                                                                              AS discount_end,

                      -- Product category
                      CASE
                          WHEN web1.Name LIKE 'Quiltestoff%' OR web1.Name LIKE 'Bekledning%stoff%' THEN 'Stoffer'
                          WHEN web1.Name LIKE N'mønster%' OR web1.Name LIKE N'Quiltemønster%' OR web1.Name LIKE N'Bekledning%mønster%' THEN N'Mønster'
                          WHEN web1.Name LIKE N'Tilbehør%' OR web1.Name LIKE 'Lim%' OR web1.Name LIKE N'Glidelås%' OR web1.Name LIKE 'Merkepenn%' OR web1.Name LIKE 'Linjal%' OR web1.Name LIKE 'Saks%' OR web1.Name LIKE N'Nål%' OR
                               web1.Name LIKE N'Skjærekniv%' OR web1.Name LIKE N'skjærematte%' OR web1.Name LIKE N'Vesketilbehør%' OR web1.Name LIKE 'Lampe%' OR web1.Name LIKE 'Strykejern%' OR web1.Name LIKE 'paper%piecing%' OR
                               web1.Name LIKE N'bånd%' OR web1.Name LIKE 'Diverse%' THEN N'Tilbehør'
                          WHEN web1.Name LIKE N'bøker%blader%' THEN N'Bøker og blader'
                          WHEN web1.Name LIKE N'Symaskin%' OR web1.Name LIKE N'Symaskintilbehør%' OR art.Name LIKE '%janome%' THEN N'Symaskiner'
                          WHEN web1.Name LIKE N'Tråd og broderigarn%' OR web1.Name LIKE N'Tråd%' OR web1.Name LIKE 'Broderigarn' THEN N'Tråd og broderigarn'
                          WHEN web1.Name LIKE N'Vatt og stabilisering%' OR web1.Name LIKE 'Vatt%' OR web1.Name LIKE 'Stabilisering%' THEN N'Vatt og stabilisering' END                AS product_category,

                      -- Product group 1
                      CASE
                          -- Stoffer
                          WHEN web1.Name LIKE 'Quiltestoff%' OR (art.Name LIKE '%stoffpakke%' OR web2.Name LIKE '%stoffpakke%' OR web3.Name LIKE '%stoffpakke%') THEN 'Quiltestoffer'
                          WHEN web1.Name LIKE 'Bekledning%stoff%' THEN 'Bekledningstoff'

                          -- Mønster
                          WHEN web1.Name LIKE N'Quiltemønster%' THEN N'Quiltemønster'
                          WHEN web1.Name LIKE N'%mønster%klær%' OR web1.Name LIKE N'Bekledning%mønster%' THEN N'Bekledningsmønster'

                          -- Tilbehør
                          WHEN web1.Name LIKE '%lim%' OR web2.Name LIKE '%lim%' THEN 'Lim'
                          WHEN web1.Name NOT LIKE 'symaskin%' AND (web1.Name LIKE N'glidelås%' OR web2.Name LIKE N'glidelås%' OR art.Name LIKE N'%glidelås%') THEN N'Glidelås'
                          WHEN web1.Name LIKE 'merkepenn%' OR web2.Name LIKE 'merkepenn%' OR web3.Name LIKE 'merkepenn%' OR art.Name LIKE '%merkepenn%' THEN 'Merkepenn'
                          WHEN web1.Name NOT LIKE 'symaskin%' AND (web1.Name LIKE 'Linjaler' OR web2.Name LIKE 'Linjaler') THEN 'Linjal'
                          WHEN web1.Name LIKE 'Saks%' OR web2.Name LIKE 'Saks%' THEN 'Sakser'
                          WHEN web1.Name NOT LIKE 'symaskin%' AND (web1.Name LIKE N'Nål%' OR web2.Name LIKE N'Nål%') THEN N'Nåler'
                          WHEN web1.Name LIKE N'%skjærekniv%' OR web2.Name LIKE N'%skjærekniv%' THEN N'Skjærekniver'
                          WHEN web1.Name LIKE N'%skjærematte%' OR web2.Name LIKE N'%skjærematte%' THEN N'Skjærematter'
                          WHEN web1.Name LIKE N'Vesketilbehør' OR web2.Name LIKE N'Vesketilbehør' THEN N'Vesketilbehør'
                          WHEN web1.Name LIKE 'Lampe%' THEN 'Lampe'
                          WHEN web1.Name LIKE N'Strykejern%' OR (web1.Name LIKE N'Tilbehør' AND art.Name LIKE '%strykejern%') THEN 'Strykejern'
                          WHEN web1.Name LIKE N'%paper%piecing%%' THEN N'Paper piecing'
                          WHEN web1.Name LIKE N'bånd%' THEN N'Bånd'
                          WHEN web1.Name LIKE N'mesh%' THEN N'Mesh'
                          WHEN web1.Name LIKE N'webbing%' THEN N'Webbing'
                          WHEN web1.Name LIKE 'Diverse%' OR web1.Name LIKE N'Tilbehør' THEN 'Diverse'

                          -- Ensure NULL
                          WHEN web1.Name LIKE N'bøker%blader%' THEN N'Bøker og blader'

                          -- Symaskiner. Order matters.
                          WHEN web1.Name LIKE N'Symaskintilbehør' OR art.ArticleID IN (46439, 47303, 47304, 47305, 47306, 47308, 47310, 47311, 47312, 47313, 47315, 44800) OR
                               ((art.Name LIKE '%symaskin%' OR art.Name LIKE '%organ%') AND web2.Name LIKE N'%Nåler%') OR web2.Name LIKE N'%Tilbehør symaskin%' THEN N'Symaskintilbehør'
                          WHEN web1.Name LIKE N'Symaskin%' OR (art.Name LIKE 'janome%' OR art.Name LIKE 'brother%' OR art.Name LIKE 'baby%lock%') THEN N'Symaskiner'

                          -- Tråd og broderigarn
                          WHEN web1.Name LIKE 'Broderi%' OR (web1.Name LIKE N'Tråd og broderigarn%' AND art.Name LIKE N'%broderi%') THEN N'Broderigarn'
                          WHEN web1.Name LIKE N'Tråd%' OR (web1.Name LIKE N'Tråd og broderigarn%' AND art.Name LIKE N'%tråd%') THEN N'Tråd'

                          -- Vatt og stabilisering
                          WHEN web1.Name LIKE 'Vatt%' OR (web1.Name LIKE N'Vatt og stabilisering%' AND art.Name LIKE '%vatt%') THEN N'Vatt'
                          WHEN web1.Name LIKE 'stabilisering%' OR (web1.Name LIKE N'Vatt og stabilisering%' AND art.Name LIKE '%stabilisering%') THEN N'Stabilisering' END            AS product_group1,

                      -- Product group 2
                      CASE
                          -- Ensure NULL
                          WHEN web1.Name LIKE N'bøker%blader%' THEN NULL
                          WHEN web1.Name LIKE 'vatt%' THEN NULL
                          WHEN web1.Name LIKE 'Stabilisering%' THEN NULL
                          WHEN web1.Name LIKE 'Broderi%' THEN NULL
                          WHEN web1.Name LIKE 'Stabilisering%' THEN NULL
                          WHEN web1.Name LIKE N'Tråd%' THEN NULL

                          -- QuilteStoff and Bekledningstoff
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE '%Halvlin%' OR art.Name LIKE '%halvlin%') THEN 'Halvlin'
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE '%Japansk%vevd%' OR art.Name LIKE '%japansk%vevd%') THEN 'Bomull'
                          WHEN web1.Name LIKE '%stoff%' AND web2.Name LIKE '%Viscose%' THEN 'Viscose'
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE 'Bomull' OR web3.Name LIKE 'Bomull' OR art.Name LIKE '%cotton%' OR art.Name LIKE '%bomull%' OR art.Description LIKE '%bomull%') THEN 'Bomull'
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE 'lin%' OR art.Name LIKE '%lin%' OR art.Description LIKE ' lin%') THEN 'Lin'
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE 'ull' OR web3.Name LIKE 'ull' OR art.Name LIKE '%wool%' OR art.Name LIKE '%ull%') THEN 'Ull'

                          -- Mønster
                          WHEN web2.Name LIKE N'Mønster barn' OR (web1.Name LIKE N'mønster%' AND web2.Name LIKE 'Barn%') THEN N'Mønster barn'
                          WHEN web2.Name LIKE N'Mønster voksen' OR (web1.Name LIKE N'mønster%' AND web2.Name LIKE 'Voksen') THEN N'Mønster voksen'

                          -- Tilbehør
                          WHEN web2.Name LIKE N'Knappenål%' OR ((web1.Name LIKE N'Tilbehør' OR web2.Name LIKE N'nål%') AND (art.Name LIKE N'%knappenål%' OR web2.Name LIKE N'Knappenål%' OR web3.Name LIKE N'knappenål%')) THEN N'Knappenåler'
                          WHEN web2.Name LIKE N'Håndsømnål%' OR ((web1.Name LIKE N'Tilbehør' OR web2.Name LIKE N'nål%') AND (art.Name LIKE N'%Håndsømnål%' OR web2.Name LIKE N'Håndsømnål%' OR art.Name LIKE N'%håndsøm%nål%'))
                              THEN N'Håndsømnåler'
                          WHEN web2.Name LIKE N'Broderinål%' OR ((web1.Name LIKE N'Tilbehør' OR web2.Name LIKE N'nål%') AND (art.Name LIKE '%embroider%needle%' OR art.Name LIKE N'%broderinål%') AND NOT art.ArticleID IN (44644))
                              THEN N'Broderinåler'
                          WHEN web2.Name LIKE N'Quiltenål%' OR ((web1.Name LIKE N'Tilbehør' OR web2.Name LIKE N'nål%') AND (art.Name LIKE '%quilt%needle%' OR art.Name LIKE N'%quiltenål%')) THEN N'Quiltenåler'
                          WHEN web2.Name LIKE N'Applikasjonsnål%' OR ((web1.Name LIKE N'Tilbehør' OR web2.Name LIKE N'nål%') AND (art.Name LIKE N'%applik%nål%' OR art.Name LIKE '%appliq%needle%')) THEN N'Applikasjonsnåler'

                          -- Bøker og blader
                          WHEN web1.Name LIKE N'bøker%blad%' AND web2.Name LIKE '%quilt%' THEN 'Quilt'
                          WHEN web1.Name LIKE N'bøker%blad%' AND web2.Name LIKE '%bekled%' THEN 'Bekledning'
                          WHEN web1.Name LIKE N'bøker%blad%' THEN 'Annet'

                          -- Symaskiner (Order is important!)
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%Sy%Broderi%' OR art.ArticleID IN (54187, 54190, 54209, 54174, 45412, 45411, 46689, 45413)) THEN 'Sy- og Broderimaskin'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%Broderimaskin%' OR art.ArticleID IN (54185, 54188, 54189, 54173, 54208, 51701, 47266)) THEN 'Broderimaskin'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%ScaNCut%' OR art.ArticleID IN (54177, 54178)) THEN 'ScaNCut'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%coverlock%' OR art.ArticleID IN (54817, 53134, 53579, 47135, 54816, 46877, 56291)) THEN 'Coverlock'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%overlock%' OR art.ArticleID IN (53133, 55014, 49352, 53132, 54812, 54813, 54814, 54815, 54210, 47285, 46825)) THEN 'Overlock'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%elektronisk%' OR art.ArticleID IN (54172, 54203,
                                                                                                                      54204, 54205,
                                                                                                                      54186, 54201,
                                                                                                                      54199, 54200,
                                                                                                                      54175, 54180,
                                                                                                                      54202, 54179,
                                                                                                                      54181, 54207,
                                                                                                                      54182, 54206,
                                                                                                                      54191, 54176,
                                                                                                                      51734, 50601, 1034,
                                                                                                                      46799, 46797,
                                                                                                                      50605, 46669,
                                                                                                                      47284, 45414,
                                                                                                                      47090, 47089,
                                                                                                                      46914, 55897, 56292, 46798)) THEN 'Elektronisk'
                          WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%mekanisk%' OR art.ArticleID IN (54183, 54198, 1012, 54165, 54163, 54164, 54162, 54159, 54160, 46867, 50604, 1072)) THEN 'Mekanisk'
                          WHEN web2.Name LIKE 'Fotpedal' OR (web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Fotpedal%') THEN 'Fotpedal'
                          WHEN web2.Name LIKE N'symaskinnål%' OR web3.Name LIKE N'%Symaskinnåler%' OR (web1.Name LIKE 'symaskin%' AND (art.Name LIKE N'%nåler%' OR web2.Name LIKE N'Nål%')) THEN N'Symaskinnåler'
                          WHEN web2.Name LIKE N'Trykkføtter%' OR art.ArticleID IN (54836, 54847, 54828, 56303, 53593, 53594, 54134) OR (web1.Name LIKE N'symaskintilbehør' AND
                                                                                                                                        (art.Name LIKE '%fot%' OR art.Name LIKE '%Foot%' OR art.Name LIKE '%acufeed%' OR
                                                                                                                                         art.Name LIKE N'%transportør%' OR art.Name LIKE N'%linjal%' OR art.Name LIKE '%guide%' OR
                                                                                                                                         art.Name LIKE '%rynkeapparat%')) THEN N'Trykkføtter'
                          WHEN web1.Name LIKE N'symaskintilbehør' OR art.ArticleID IN (46439) THEN N'Diverse symaskintilbehør' END                                                    AS product_group2,

                      -- Product group 3
                      CASE
                          -- Ensure NULL
                          WHEN web1.Name LIKE N'bøker%blader%' THEN NULL
                          WHEN web1.Name LIKE 'vatt%' THEN NULL
                          WHEN web1.Name LIKE 'Stabilisering%' THEN NULL
                          WHEN web1.Name LIKE 'Broderi%' THEN NULL
                          WHEN web1.Name LIKE 'Stabilisering%' THEN NULL
                          WHEN web1.Name LIKE N'Tråd%' THEN NULL

                          -- Stoff
                          WHEN web1.Name LIKE '%stoff%' AND (art.Name LIKE '%stoffpakke%' OR web2.Name LIKE '%stoffpakke%') THEN 'Stoffpakke'
                          WHEN web1.Name LIKE '%stoff%' AND web2.Name LIKE '%baksidestoff%' THEN 'Baksidestoff'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (art.Name LIKE '%interlock%' OR web2.Name LIKE '%interlock%' OR web3.Name LIKE '%interlock%') THEN N'Interlock'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Rib' OR web3.Name LIKE 'Rib') THEN 'Rib'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'French Terry' OR web3.Name LIKE 'French Terry') THEN 'French Terry'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Melert%' OR web3.Name LIKE 'Melert%' or art.Name LIKE '%melert%') THEN 'Melert'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Essex%' OR web3.Name LIKE 'Essex%') THEN 'Essex'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'batik%' OR web3.Name LIKE 'batik%' OR web2.Name LIKE '%batik%' OR art.Name LIKE '%batik%') THEN 'Batikk'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Chambray%' OR web3.Name LIKE 'Chambray%' OR web2.Name LIKE N'Chambray') THEN N'Chambray'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Jersey%' OR web3.Name LIKE 'Jersey%') THEN 'Jersey'
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE '%Japansk%vevd%' OR art.Name LIKE '%japansk%vevd%') THEN 'Japanske vevde'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'Vevd%' OR web3.Name LIKE 'Vevd%' OR web2.Name LIKE N'Vevd%' OR web2.Name LIKE '%vevd%') THEN N'Vevde stoffer'
                          WHEN (web1.Name LIKE '%stoff%' OR web1.Name LIKE '%jersey%') AND (web2.Name LIKE 'trykte stoffer' OR web3.Name LIKE 'trykte stoffer' OR web2.Name LIKE 'trykte stoffer') THEN 'Trykte stoffer'

                          -- Seasonal before trykte stoffer in order to avoid override.
                          WHEN web1.Name LIKE '%stoff%' AND (web2.Name LIKE N'påske%' OR web3.Name LIKE N'påske%') THEN N'Påskestoffer'
                          WHEN web1.Name LIKE '%stoff%' AND (art.Name LIKE '%christmas%' OR art.Name LIKE '%jul%' OR web2.Name LIKE 'Jul%' OR web3.Name LIKE 'Jul%') THEN 'Julestoffer'

                          -- Mønstre
                          WHEN web1.Name LIKE N'%mønster%' AND (art.Name LIKE '%christmas%' OR art.Name LIKE '%jul%' OR web2.Name LIKE 'Jul%' OR web3.Name LIKE 'Jul%') THEN N'Julemønster'
                          WHEN web1.Name LIKE N'%mønster%' AND (web2.Name LIKE N'påske%' OR web3.Name LIKE N'påske%') THEN N'Påskemønster'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Bag%' THEN 'Bagger'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'veske%' THEN 'Vesker'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Teppe%' THEN 'Tepper'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE N'Løper%' THEN N'Løper'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Pung%' THEN 'Punger'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Pute%' THEN 'Puter'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Mappe%' THEN 'Mapper'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Spisebrikke%' THEN 'Spisebrikker'
                          WHEN web1.Name LIKE N'%mønster%' AND web3.name LIKE 'Duker%' THEN 'Duker'

                          -- Symaskintilbehør
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE N'Kantbåndapp%' OR art.Name LIKE N'%Kan%bånd%' OR art.Name LIKE N'Faldesømbrett%') THEN N'Kantbåndapparat'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Trykkfotfest%' OR art.Name LIKE N'%trykkfotfeste%') THEN N'Trykkfotfeste'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Kniv%' OR art.Name LIKE N'%kniv%') THEN N'Kniv'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Spolestopp%' OR art.Name LIKE '%spolestopper%') THEN N'Spolestopper'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Sybord%' OR art.Name LIKE '%sybord%') THEN 'Sybord'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Belysning%' OR art.Name LIKE '%lys%') THEN N'Belysning'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Symaskinmatt%' OR art.Name LIKE '%matte%') THEN N'Symaskinmatte'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE N'Nålepute%' OR art.Name LIKE N'%nålpute%' OR art.Name LIKE N'%Nålepute%') THEN N'Nålepute'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Spolehus%' OR art.Name LIKE '%spolehus%') THEN N'Spolehus'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Spolehold%' OR art.Name LIKE '%spoleholder%') THEN N'Spoleholder'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Programvare%' OR art.Name LIKE '%brother%pe%design%') THEN 'Programvare'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Oppgradering%' OR art.Name LIKE '%oppgradering%') THEN 'Oppgraderingssett'
                          WHEN web1.Name LIKE N'symaskintilbehør' AND (web3.Name LIKE 'Utstyr%boks%' OR art.Name LIKE N'%boks%') THEN N'Utstyrsboks' END                              AS product_group3,

                      -- Product color
                      CASE
                          -- Only colors for stoff
                          WHEN web1.Name NOT LIKE N'%stoff%' THEN NULL

                          WHEN web1.Name LIKE N'mønster%' OR web1.Name LIKE '%symaskin%' OR web1.Name LIKE N'Tilbehør' THEN NULL
                          WHEN web2.Name LIKE 'gull' OR web3.Name LIKE 'gull%' OR art.Name LIKE '%gold%' OR art.Name LIKE N'%gull%' THEN N'Gull'
                          WHEN web2.Name LIKE N'sølv' OR web3.Name LIKE N'sølv%' OR art.Name LIKE '%silver%' OR art.Name LIKE N'%sølv%' THEN N'Sølv'
                          WHEN web2.Name LIKE N'grønn' OR web3.Name LIKE N'grønn%' OR art.Name LIKE '%green%' OR art.Name LIKE N'%grønn%' THEN N'Grønn'
                          WHEN web2.Name LIKE 'gul' OR web3.Name LIKE 'gul%' OR art.Name LIKE '%yellow%' OR art.Name LIKE '%gul%' THEN N'Gul'
                          WHEN web2.Name LIKE 'hvit%' OR web3.Name LIKE 'hvit%' OR web2.Name LIKE ' %offwhite%' OR web3.Name LIKE '%offwhite%' OR art.Name LIKE '%white%' OR art.Name LIKE '%hvit%' THEN N'Hvit'
                          WHEN web2.Name LIKE N'rød%' OR web3.Name LIKE N'rød%' OR art.Name LIKE '% red%' OR art.Name LIKE N'%rød%' THEN N'Rød'
                          WHEN web2.Name LIKE 'beige' OR web3.Name LIKE 'beige%' OR art.Name LIKE '%cream%' OR art.Name LIKE '%beige%' THEN N'Beige'
                          WHEN web2.Name LIKE '%brun%' OR web3.Name LIKE 'brun%' OR art.Name LIKE '%brown%' OR art.Name LIKE '%brun%' OR art.Name LIKE '%tan%' THEN N'Brun'
                          WHEN web2.Name LIKE 'orange' OR web3.Name LIKE 'orange%' OR art.Name LIKE '%orange%' OR art.Name LIKE N'%oransje%' THEN N'Oransje'
                          WHEN web2.Name LIKE N'blå' OR web3.Name LIKE N'blå%' OR art.Name LIKE '%blue%' OR art.Name LIKE N'%blå%' OR art.Name LIKE '%sky%' OR art.Name LIKE '%navy%' THEN N'Blå'
                          WHEN web2.Name LIKE 'sort' OR web3.Name LIKE 'sort%' OR web2.Name LIKE 'svart%' OR web3.Name LIKE 'svart%' OR art.Name LIKE '%black%' OR art.Name LIKE N'%sort%' OR art.Name LIKE '%svart%' THEN N'Svart'
                          WHEN web2.Name LIKE 'lilla%' OR web3.Name LIKE 'lilla%' OR art.Name LIKE '%purple%' OR art.Name LIKE '%lilla%' THEN N'Lilla'
                          WHEN web2.Name LIKE 'rosa' OR web3.Name LIKE '%Rosa%' OR art.Name LIKE '%pink%' OR art.Name LIKE N'%rosa%' THEN N'Rosa'
                          WHEN web2.Name LIKE N'grå' OR web3.Name LIKE N'grå%' OR art.Name LIKE '%grey%' OR art.Name LIKE N'%grå%' OR art.Name LIKE '%charcoal%' THEN N'Grå'
                          WHEN web2.Name LIKE 'ensfarge%' THEN 'Ensfarget' END                                                                                                        AS 'product_color',

                      -- Designer or product series
                      CASE
                          -- Fixme: Add from Producer/brand below?
                          WHEN prl.Name IS NOT NULL THEN prl.Name
                          Else 'Andre' END                                                                                                                                            AS 'designer',

                      -- Supplier / Leverandør
                      CASE WHEN sup.SupplierID IN (1, 3) THEN sup.Name END                                                                                                            AS 'supplier',

                      -- Producer / Brand
                      CASE

                          WHEN art.Name LIKE '%janome%' OR art.Name LIKE '%jabome%' OR art.Name LIKE '%Janbome%' OR art.Name LIKE '%Jasbome%' THEN 'Janome'
                          WHEN art.Name LIKE '%baby%lock%' OR web2.Name LIKE 'baby%lock%' THEN 'Baby Lock'
                          WHEN art.Name LIKE '%brother%' THEN 'Brother'
                          WHEN art.Name LIKE '%prym%' THEN 'Prym'
                          WHEN art.Name LIKE '%guterman%' OR art.Name LIKE '%gutterman%' THEN N'Gütermann'
                          WHEN art.Name LIKE '%Organ needle%' THEN 'Organ Needles'

                          WHEN man.Name IS NOT NULL THEN man.Name

                          -- Fixme: Check all these below
                          WHEN sup.Name LIKE '%byannie%' THEN 'By Annie'
                          WHEN sup.Name LIKE '%annaka%' THEN 'AnnAKa'
                          WHEN sup.Name LIKE 'Sew kind of wonderful' THEN 'Sew kind of wonderful'
                          WHEN sup.Name LIKE 'Jen Kingwell' THEN 'Jen Kingwell'
                          WHEN sup.Name LIKE 'Red Brolly' THEN 'Red Brolly'
                          WHEN sup.Name LIKE 'Bente Tufte' THEN 'Bente Tufte'
                          WHEN sup.Name LIKE 'Ryum Quilt' THEN 'Ryum Quilt'
                          WHEN sup.Name LIKE N'FR Jørgensen' THEN N'FR Jørgensen'
                          WHEN sup.Name LIKE 'Per Olden' THEN 'Per Olden'
                          WHEN sup.Name LIKE 'Villy Jensen' THEN 'Villy Jensen'
                          WHEN sup.Name LIKE 'Th. Ellebye' THEN 'Th. Ellebye'
                          WHEN sup.Name LIKE 'Hjelmtvedt' THEN 'Hjelmtvedt'
                          WHEN sup.Name LIKE 'Bente Malm' THEN 'Bente Malm'
                          WHEN sup.Name LIKE 'Creative Grids' THEN 'Creative Grids'
                          WHEN sup.Name LIKE 'Sue Daley' THEN 'Sue Daley'
                          WHEN sup.Name LIKE 'Solbritt & Maria' THEN 'Solbritt & Maria'
                          WHEN sup.Name LIKE 'Adlico' THEN 'Adlico'
                          WHEN sup.Name LIKE 'Stof' THEN 'Stof'
                          WHEN sup.Name LIKE 'Tyger & Ting' THEN 'Tyger & Ting'
                          WHEN sup.Name LIKE 'Lynette Andersons%' THEN 'Lynette Andersons'
                          WHEN sup.Name LIKE '%Berry Creations%' THEN 'Fign Berry Creations'
                          WHEN sup.Name LIKE 'Hatched & Patched' THEN 'Hatched & Patched'

                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Jaybird Quilt%' THEN 'Jaybird Quilts'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Lori Holt%' THEN 'Lori Holt'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Jelly Roll%' THEN 'Sweetwater'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Cottage Garden Threads%' THEN 'Cottage Garden Threads'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Sew Kind of Wonderful%' THEN 'Sew Kind of Wonderful'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Alison Glass%' THEN 'Alison Glass'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Amy Bradley Designs%' THEN 'Amy Bradley Designs'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Bird Brain%' THEN 'Bird Brain'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'By Annie%' THEN 'By Annie'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Clairturpindesigns%' THEN 'Claire Turpin Designs'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Crab-Apple Hild Studio%' THEN 'Crabapple Hill Studio'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Elisabeth Hartmann%' THEN 'Elisabeth Hartmann'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Gail Pan Design%' THEN 'Gail Pan Design'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Jennifer Sampou%' THEN 'Jennifer Sampou'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Laumdry Basket Quilts%' THEN 'Laundry Basket Quilts'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Apliquick%' THEN 'Apliquick'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Laura Heine%' THEN 'Laura Heine'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Lazy Girl Design%' THEN 'Lazy Girl Design'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Leanne''s House%' THEN 'Leanne''s House'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Libs Elliot%' THEN 'Libs Elliot'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Monica Pool%' THEN 'Monica Pool'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Painted Pony''n Quilts%' THEN 'Painted Pony''n Quilts'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Sassafras Lane Design%' THEN 'Sassafras Lane Design'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Solbritt & Maria%' THEN 'Solbritt & Maria'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Studio Kat Designs%' THEN 'Studio Kat Designs'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Sue Daley%' THEN 'Sue Daley'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'The Birdhouse%' THEN 'The Birdhouse'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'The Pattern Basket%' THEN 'The Pattern Basket'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'This & That%' THEN 'This & That'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Tyger & Ting%' THEN 'Tyger & Ting'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Zen Chic%' THEN 'Zen Chic'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Fragile%' THEN 'Zen Chic'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Layer Cake%' THEN 'Zen Chic'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Peppa Pig%' THEN 'Peppa Gris'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'AnnaKa%' THEN 'AnnAKa'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Bente Malm%' THEN 'Bente Malm'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Ryum Quilt%' THEN 'Ryum Quilt'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Sewline%' THEN 'Sewline'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Minikrea%' THEN 'Minikrea'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Bente Tufte%' THEN 'Bente Tufte'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Judith Eknes%' THEN 'Judith Eknes'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Yoko Saito%' THEN 'Yoko Saito'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Tilda%' THEN 'Tildas world'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Superior Threads%' THEN 'Superior Threads'
                          WHEN COALESCE(web3.Name, web2.Name) LIKE 'Grunge%' THEN 'Basic Grey'


                          WHEN art.Name LIKE '%Avalana%' OR art.Name LIKE 'Nellies Shirtings%' OR art.Name LIKE 'Molly Roses%' THEN 'Stoffabrics'
                          WHEN art.Name LIKE '%Homespun%' THEN 'Homespun'
                          WHEN art.Name LIKE '%Country meadow%' THEN 'Pam Buda'
                          WHEN art.Name LIKE '%Northcott Canvas%' THEN 'Northcott'
                          WHEN art.Name LIKE '%Chalk and Charcoal%' THEN 'Chalk and Charcoal'
                          WHEN art.Name LIKE '%shadow play%' THEN 'Shadow Play'
                          WHEN art.Name LIKE 'Vatt' THEN 'Hobbs'
                          WHEN art.Name LIKE '%Natures Study%' THEN 'Whistler Studios'
                          WHEN art.Name LIKE '%Quilters shadow%' OR art.Name LIKE 'Melange%' THEN 'Stof Fabrics'
                          WHEN art.Name LIKE '%Kaffe Fassett%' THEN 'Kaffe Fassett'
                          WHEN art.Name LIKE '%Ladybug Mania%' THEN 'Clothworks'
                          WHEN art.Name LIKE '%Basil%' AND art.Name LIKE '%Blessings%' THEN 'Michael Miller Fabric'
                          WHEN art.Name LIKE '%Magical Winter%' OR art.Name LIKE 'RK %' THEN 'Robert Kaufman'
                          WHEN (art.Name LIKE '%Hobbs%' OR art.Name LIKE '%Heirloom%') AND web2.Name LIKE 'Vatt' THEN 'Hobbs'
                          WHEN art.Name LIKE '%Bohemian blue%' THEN 'Wilmington Prints'
                          WHEN art.Name LIKE '%Antique Pattern Collection%' THEN 'Junko Matsuda'
                          WHEN art.Name LIKE '%Michael miller%' THEN 'Michael miller'
                          WHEN art.Name LIKE '%Makeover UK%' THEN 'Makower UK'
                          WHEN art.Name LIKE '%marcus%' AND art.Name LIKE '%fabrics%' THEN 'Marcus Brothers Fabrics'
                          WHEN art.Name LIKE '%Zen Chic%' THEN 'Zen Chic'
                          WHEN art.Name LIKE N'%Fæbrik%' THEN N'Fæbrik'
                          Else 'Andre' END                                                                                                                                            AS brand,

                      CASE WHEN CAST(CURRENT_TIMESTAMP - art.LastUpdate AS INT) < 120 AND (art.ArticleID > (SELECT MAX(ArticleID) FROM Articles) - 500) THEN 'Nyhet' END              AS new_tag

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
                           LEFT JOIN ProductLines prl ON prl.ProductLineID = art.ProductLineID
                  WHERE art.Status = 0
                    AND ((art.VisibleOnWeb = 1 AND art.Picture IS NOT NULL) OR (art.Name LIKE '%Brother%' OR art.Name LIKE '%baby%lock%' OR art.Name LIKE '%Janome%' OR art.Name LIKE '%organ%')))
SELECT sku,
       barcode,
       TRIM(title)                                                                                                                                                                                                          as title,
       CASE WHEN price_unit LIKE 'meter' THEN ROUND(CAST(price AS FLOAT) / 10.0, 1) WHEN price IS NULL THEN 0 ELSE price END                                                                                                AS price,
       IIF(price_unit LIKE 'meter%', 'desimeter', ISNULL(price_unit, 'stk'))                                                                                                                                                AS price_unit,
       IIF(NOT available > 0 OR available IS NULL, 0, available)                                                                                                                                                            AS available,
       body_html,
       images,
       product_category,
       product_group1,
       product_group2,
       product_group3,
       IIF(product_category LIKE 'stoff%', product_group2, NULL)                                                                                                                                                            AS fabric_material,
       IIF(product_category LIKE 'stoff%', product_group3, NULL)                                                                                                                                                            AS fabric_type,
       IIF(product_category LIKE 'stoff%', product_color, NULL)                                                                                                                                                             AS product_color,
       IIF(product_category LIKE N'%mønster%', product_group3, NULL)                                                                                                                                                        AS pattern_type,
       supplier, -- Supplier / Leverandør (Amendo)
       brand,    -- Brand / Produsent (Amendo)
       vat_rate                                                                                                                                                                                                              AS vat_rate,
       CASE
           WHEN price_unit LIKE 'meter' THEN ROUND(CAST(purchase_price AS FLOAT) / 10.0, 1)
           WHEN purchase_price IS NULL THEN 0
           ELSE purchase_price END AS cost_price,
       CASE WHEN price_unit LIKE 'Meter' THEN 11 WHEN price_unit LIKE 'Stk' THEN 1 WHEN price_unit LIKE 'PK' THEN 2 ELSE 1 END                                                                                              AS amendo_price_unit_id,

       designer,
       hide_when_empty,
       CASE WHEN discount_start < CURRENT_TIMESTAMP AND CURRENT_TIMESTAMP < discount_end AND discounted_price > 0 THEN IIF(price_unit LIKE 'meter', ROUND(CAST(discounted_price AS FLOAT) / 10.0, 1), discounted_price) END AS discounted_price,
       CONCAT(product_category, ',', product_group1, ',', product_group2, ',', product_group3, ',', product_color, ',', brand, ',', designer, ',', new_tag, ',', IIF(price_unit LIKE 'meter%', 'metervare', 'stykkvare'))   AS tags,
       source_updated

FROM Products pro
WHERE sku NOT IN (45413, 49352, 51701, 53655)
  AND ((NOT (price < 10 AND available <= 0)) OR (barcode in ('796402004', '788013009', '102738', '102326', '102324', '185330')))
  AND NOT (brand LIKE 'Brother' AND available <= 0)

ORDER BY sku
;