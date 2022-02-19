WITH Products AS (
    SELECT
        -- Product
        art.Description                                                                 AS body_html,
        art.Picture                                                                     AS images,
        art.Name                                                                        AS title,

        -- ProductVariant
        art.ArticleNo                                                                   AS sku,
        art.ArticleID                                                                   AS source_id,
        art.LastUpdate                                                                  AS source_updated,
        CASE
            WHEN grp.MainGroupID = 10 THEN CAST(art.SalesPrice AS FLOAT)
            ELSE CAST(art.SalesPrice AS FLOAT) * 1.25
            END                                                                         AS price,
        CASE
            WHEN COALESCE(art_com.Name2, art.PriceUnit) LIKE 'meter%' THEN 'meter'
            WHEN art.PriceUnit = '' THEN 'stk'
            ELSE art.PriceUnit
            END                                                                         AS price_unit,
        CASE
            WHEN COALESCE(IIF(art_com.Name2 LIKE 'meter%', 'meter', NULL), art.PriceUnit) LIKE 'meter%'
                THEN FLOOR((CAST(ISNULL(rec.C, 0) AS FLOAT) - CAST(ISNULL(sol.C, 0) AS FLOAT)) * 10.0)
            ELSE FLOOR(ISNULL(rec.C, 0) - ISNULL(sol.C, 0))
            END                                                                         AS available,
        CASE
            WHEN grp.Name LIKE 'symaskiner' OR grp.Name LIKE N'symaskintilbehør' THEN 0
            ELSE 1
            END                                                                         AS hide_when_empty,
        CASE WHEN art.OfferPrice > 0 THEN IIF(grp.MainGroupID = 10, CAST(art.OfferPrice AS FLOAT), CAST(art.OfferPrice AS FLOAT) * 1.25) END                            AS discounted_price,
        art.StartOfferPrice                                                             AS discount_start,
        art.StopOfferPrice                                                              AS discount_end,
        CASE
            WHEN web1.Name LIKE N'bøker%blader%' THEN N'Bøker og blader'
            WHEN web1.Name LIKE N'mønster%' THEN N'Mønster'
            WHEN web1.Name LIKE 'Quiltestoffer' OR (art.Name LIKE '%stoffpakke%' OR web2.Name LIKE '%stoffpakke%' OR web3.Name LIKE '%stoffpakke%') THEN 'Quiltestoff'
            WHEN web1.Name LIKE 'Bekledningsstoff%' OR (web1.Name LIKE 'Jersey%' OR art.Name LIKE '%french%terry%' OR art.Name LIKE '%Interlock%' OR art.Name LIKE '%viscose%') THEN 'Bekledningsstoff'  -- Fixme: Stoff vs. Bekledningsstoff?

            -- Order matters for Symaskin.
            WHEN web1.Name LIKE N'Symaskintilbehør' OR ((art.Name LIKE '%symaskin%' or art.Name LIKE '%organ%') AND web2.Name LIKE N'%Nåler%') OR web2.Name LIKE N'%Tilbehør symaskin%' THEN N'Symaskintilbehør'
            WHEN web1.Name LIKE N'Symaskin%' OR (art.Name LIKE 'janome%' OR art.Name LIKE 'brother%' OR art.Name LIKE 'baby%lock%') THEN N'Symaskiner'

            WHEN web1.Name LIKE N'Tilbehør%' OR web2.Name LIKE N'%Nåler%' THEN N'Tilbehør'
            WHEN web1.Name LIKE N'Vatt og stabilisering%' THEN N'Vatt og stabilisering'
            WHEN web1.Name LIKE N'Tråd og broderigarn%' THEN N'Tråd og broderigarn'

            ELSE CONCAT('deleteme: ', web1.Name)
            END                                                                         AS product_type,
        CASE
            -- Ensure NULL
            WHEN web1.Name LIKE N'bøker%blader%' THEN NULL

            -- Symaskiner (Order is important!)
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%Sy%Broderi%' OR art.ArticleID IN (54187, 54190, 54209, 54174, 45412, 45411, 46689)) THEN 'Sy- og Broderimaskin'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%Broderimaskin%' OR art.ArticleID IN (54185, 54188, 54189, 54173, 54208, 51701, 47266)) THEN 'Broderimaskin'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%ScaNCut%' OR art.ArticleID IN (54177, 54178)) THEN 'ScaNCut'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%coverlock%' OR art.ArticleID IN (54817, 53134, 53579, 47135, 54816, 46877)) THEN 'Coverlock'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%overlock%' OR art.ArticleID IN (53133, 55014, 49352, 53132, 54812, 54813, 54814, 54815, 54210, 47285, 46825)) THEN 'Overlock'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%elektronisk%' OR art.ArticleID IN (54172, 54203, 54204, 54205, 54186, 54201, 54199, 54200, 54175, 54180, 54202, 54179, 54181, 54207, 54182, 54206, 54191, 54176, 51734, 50601, 1034, 46799, 46797, 50605, 46669, 47284, 45414, 47090, 47089, 46914, 55897)) THEN 'Elektronisk'
            WHEN web1.Name LIKE N'Symaskiner%' AND (web2.Name LIKE '%mekanisk%' OR art.ArticleID IN (54183, 54198, 1012, 54165, 54163, 54164, 54162, 54159, 54160, 46867, 50604, 1072)) THEN 'Mekanisk'

            -- Symaskintilbehør
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Fotpedal%' THEN 'Fotpedal'
            WHEN web1.Name LIKE N'symaskintilbehør' AND (
                (art.Name LIKE '%fot%' AND art.Name NOT LIKE '%pedal%') OR
                art.Name LIKE '%acufeed%' OR
                art.Name LIKE '%apparat%' OR
                art.Name LIKE N'%transportør%' OR
                art.Name LIKE N'%linjal%' OR
                art.Name LIKE '%guide%' OR
                art.Name LIKE N'%Kantbånd%' OR
                art.Name LIKE N'%bretter%' OR
                art.ArticleID IN (54836, 54847, 54828)
                )
                THEN N'Trykkføtter'
            WHEN (web2.Name LIKE N'%Nåler%' AND web1.Name LIKE '%symaskin%') OR web3.Name LIKE N'%Symaskinnåler%' THEN N'Symaskinnåler'

            -- QuilteStoff and Bekledningsstoff
            WHEN art.Name LIKE '%stoffpakke%' OR web2.Name LIKE '%stoffpakke%' OR web3.Name LIKE '%stoffpakke%' THEN 'Stoffpakke'
            WHEN web2.Name LIKE '%Halvlin%' THEN 'Halvlin'

            -- Mønster
            WHEN web1.Name LIKE N'mønster%' AND web2.Name LIKE '%quilt%' THEN N'Quiltemønster'
            WHEN web1.Name LIKE N'mønster%' AND web2.Name LIKE '%bekledning%' THEN N'Bekledningsmønster'

            -- Tilbehør
            WHEN web2.Name LIKE 'Sakser' THEN 'Sakser'
            WHEN web2.Name LIKE 'Linjaler' THEN 'Linjal'
            WHEN web2.Name LIKE N'%skjærekniver%' OR web2.Name LIKE N'%skjærematter%' THEN N'Skjærekniver- og skjærematter'  -- Fixme: Okay name?
            WHEN web2.Name LIKE N'%Nåler%' THEN N'Nåler'
            WHEN web2.Name LIKE '%lim%' THEN 'Lim'
            WHEN web3.Name LIKE '%merkepenn%' OR web2.Name LIKE '%merkepenn%' OR art.Name LIKE '%merkepenn%' THEN 'Merkepenn'
            WHEN web1.Name LIKE N'Tilbehør' AND art.Name LIKE '%strykejern%' THEN 'Strykejern'
            WHEN web2.Name LIKE N'Vesketilbehør' THEN N'Vesketilbehør'
            WHEN web2.Name LIKE N'%glidelås%' OR art.Name LIKE N'%glidelås%' THEN N'Glidelås'

            -- Vatt og stabilisering
            WHEN web1.Name LIKE N'Vatt og stabilisering%' AND (web2.Name LIKE 'Stabilisering' or art.Name LIKE '%Stabilisering%') THEN N'Stabilisering'
            WHEN web1.Name LIKE N'Vatt og stabilisering%' AND (web2.Name LIKE 'Vatt' or art.Name LIKE '%Vatt%')THEN N'Vatt'

            -- Tråd og broderigarn
            WHEN web2.Name LIKE N'%håndquiltetråd%' THEN N'Håndquiltetråd'
            WHEN web2.Name LIKE N'Applikasjonstråd%' THEN N'Applikasjonstråd'
            -- Fixme: Elastisk tråd
            -- Fixme: Sytråd
            -- Fixme: Broderigarn

            ELSE CONCAT('deleteme: ', web2.Name)
            END                                                                         AS product_subtype,
        CASE
            -- Ensure NULL
            WHEN web1.Name LIKE N'bøker%blader%' THEN NULL

            -- Symaskintilbehør
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%matte%' THEN N'Symaskinmatte'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%spolehus%' THEN N'Spolehus'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%spolestopper%' THEN N'Spolestopper'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%spoleholder%' THEN N'Spoleholder'
            WHEN web1.Name LIKE N'symaskintilbehør' AND web2.Name LIKE 'diverse' AND art.Name LIKE '%lys%'
                THEN N'Belysning'
            WHEN art.Name LIKE '%spoleholder%' THEN 'Spoleholder'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%oppgradering%' THEN 'Oppgraderingssett'
            WHEN web1.Name LIKE N'symaskintilbehør' AND (art.Name LIKE N'%nålpute%' OR art.Name LIKE N'%Nålepute%') THEN N'Nålepute'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%brother%pe%design%' THEN 'Programvare'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%glidefot%' THEN 'Glidefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%Frihånd%' THEN N'Frihånds-quiltefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%glidelåsfot%' THEN N'Glidelåsfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%rynke%' THEN 'Rynkefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%snor%fot%' THEN 'Snorfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%sik%sak%%' THEN 'Sikksakkfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%stoff%guide%%' THEN 'Stoff-guide'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%rettsøm%' THEN N'Rettsømfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%1/4%' THEN '1/4-inch'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%applikasjon%' THEN 'Applikasjonsfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Bise%' THEN 'Bisefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Blind%' THEN 'Blindstingfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Ditch%' THEN 'Ditch-quiltefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Linjalfot%' THEN 'Linjalfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Falde%' THEN 'Faldefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%Overlock%fot%' THEN 'Overlock-fot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%k%pp%hull%' THEN 'Knapphullsfot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%overtransport%' THEN N'Overtransportør'
            WHEN web1.Name LIKE N'symaskintilbehør' AND (art.Name LIKE '%rullefot%' OR art.Name LIKE '%roller%') THEN N'Rullefot'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%Kan%bånd%' THEN N'Kantbåndsapparat'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%sybord%' THEN 'Sybord'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE '%acufeed%' THEN 'Acufeed'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%nålitreer%' THEN N'nålitreder'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%trykkfotfeste%' THEN N'Trykkfotfeste'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%boks%' THEN N'Boks'
            WHEN web1.Name LIKE N'symaskintilbehør' AND art.Name LIKE N'%kniv%' THEN N'Kniv'

            -- Quiltestoff and Bekledningsstoff
            WHEN web1.Name LIKE '%Jersey%' AND art.Name LIKE N'%interlock%' THEN N'Interlock'
            WHEN web1.Name LIKE 'Jersey%' THEN 'Jersey'
            -- Fixme: Bomull
            -- Fixme: French Terry
            -- Fixme: Rib
            WHEN web2.Name LIKE '%Japanske vevde%' THEN 'Japanske vevde'
            WHEN web2.Name LIKE N'Vevde stoffer' OR web2.Name LIKE '%vevd%' THEN N'Vevde stoffer'
            WHEN web2.Name LIKE '%batik%' OR art.Name LIKE '%batik%' THEN 'Batikk'
            WHEN web2.Name LIKE 'bakgrunn%basis%stoffer' OR web2.Name LIKE 'baksidestoff%' THEN 'Baksidestoff'
            WHEN web2.Name LIKE 'trykte stoffer' THEN 'trykte stoffer'
            WHEN web2.Name LIKE N'Chambray' THEN N'Chambray'
            -- Påskestoff??
            -- Fixme: Melert
            -- Bekledningsstoff

            -- Fixme: Essex

            WHEN web1.Name LIKE 'Quiltestoffer' AND (art.Name LIKE '%christmas%' OR art.Name LIKE '%jul%' OR web2.Name LIKE 'Jul%' OR web3.Name LIKE 'Jul%') THEN 'Julestoff'
            -- Fixme: Barn/voksen
            -- Fixme: Påskestoff

            ELSE CONCAT('deleteme: ', web3.Name)
            END                                                                         AS product_subtype2,
        CASE
            -- Ensure NULL
            WHEN web1.Name LIKE N'bøker%blader%' THEN NULL

            -- Other tags
            WHEN web3.Name LIKE '%Mummi%' THEN 'Mummi'
            WHEN web3.Name LIKE N'%Knappenåler%' THEN N'Knappenåler'
            WHEN web3.Name LIKE N'%Synåler%' THEN N'Synåler'
            WHEN web3.Name LIKE '%Peggy%' THEN 'Peggy'
            WHEN art.Name LIKE '%handlenett%' THEN 'Handlenett'
            WHEN art.Name LIKE '%stempel%' THEN 'Stempel'
            WHEN art.Name LIKE '%strikk%' THEN 'Strikk'
            WHEN art.Name LIKE '%Applique%' OR art.Name LIKE '%applikasjon%' or web2.Name LIKE '%applikasjon%'
                THEN 'Applikasjon'
            WHEN web2.Name LIKE N'Ull til applikasjon' THEN N'Ull til applikasjon'
            WHEN art.Name LIKE '%tekstillim%' THEN 'Lim'
            WHEN art.Name LIKE '%lommelykt%' THEN 'Lys'
            WHEN art.Name LIKE '%neglefil%' THEN 'Neglefil'
            WHEN art.Name LIKE N'%skråbånd%' THEN N'Skråbånd'
            WHEN art.Name LIKE '%Strykematte%' THEN 'Strykematte'
            WHEN art.Name LIKE '%skredderkritt%' THEN 'Skredderkritt'
            WHEN art.Name LIKE N'%Målebånd%' THEN N'Målebånd'
            WHEN art.Name LIKE N'%Metalltråd%' THEN N'Metalltråd'
            WHEN art.Name LIKE N'%Skumgummivatt%' THEN N'Skumgummivatt'
            WHEN art.Name LIKE '%boks%' THEN 'boks'
            WHEN art.Name LIKE '%sprayflaske%' THEN 'Sprayflaske'
            WHEN art.Name LIKE '%gave%' THEN 'Gave'
            WHEN art.Name LIKE '%bag%' OR art.Name LIKE '%veske%' THEN 'Bag og veske'
            WHEN art.Name LIKE '%snor%' THEN 'Snor'
            WHEN art.Name LIKE '%teip%' THEN 'Teip'
            WHEN art.Name LIKE '%malje%' THEN 'Malje'

            WHEN web2.Name LIKE '%Ensfarget%' THEN 'Ensfarget'
            WHEN web2.Name LIKE 'Mesh%' OR web3.Name LIKE 'Mesh%' THEN 'Mesh'
            WHEN web2.Name LIKE 'pappmal%' THEN 'Pappmal'
            WHEN web2.Name LIKE N'skjæremaler%' THEN N'Skjæremaler'
            WHEN web3.Name LIKE 'Gaver/esker/bokser' THEN 'Gaver, esker og bokser'
            WHEN art.Name LIKE N'knappenål%' THEN N'Knappenåler'
            WHEN web3.Name LIKE N'%Peppa %' THEN 'Peppa Gris'
            WHEN web2.Name LIKE '%Layer Cake%' OR art.Name LIKE '%Layer Cake%' THEN 'Layer Cake'
            WHEN web3.Name LIKE '%tynn%dukvatt%' THEN 'Tynn dukvatt'
            WHEN web3.Name LIKE '%diverse%design%' THEN 'Diverse designere'
            WHEN web1.Name LIKE N'symaskintilbehør' THEN 'Diverse'
            END                                                                         AS product_subtype3,

        CASE
            -- NULL when mønster and tilbehør
            WHEN web1.Name LIKE N'mønster%' OR web1.Name LIKE '%symaskin%' OR web1.Name LIKE N'Tilbehør' THEN NULL

            WHEN web2.Name LIKE 'gull' OR web3.Name LIKE 'gull%' OR art.Name LIKE '%gold%' OR art.Name LIKE N'%gull%'
                THEN N'Gull'
            WHEN web2.Name LIKE N'sølv' OR web3.Name LIKE N'sølv%' OR art.Name LIKE '%silver%' OR
                 art.Name LIKE N'%sølv%' THEN N'Sølv'
            WHEN web2.Name LIKE N'grønn' OR web3.Name LIKE N'grønn%' OR art.Name LIKE '%green%' OR
                 art.Name LIKE N'%grønn%' THEN N'Grønn'
            WHEN web2.Name LIKE 'gul' OR web3.Name LIKE 'gul%' OR art.Name LIKE '%yellow%' OR art.Name LIKE '%gul%'
                THEN N'Gul'
            WHEN web2.Name LIKE 'hvit%' OR web3.Name LIKE 'hvit%' OR web2.Name LIKE ' %offwhite%' OR
                 web3.Name LIKE '%offwhite%' OR art.Name LIKE '%white%' OR art.Name LIKE '%hvit%' THEN N'Hvit'
            WHEN web2.Name LIKE N'rød%' OR web3.Name LIKE N'rød%' OR art.Name LIKE '% red%' OR art.Name LIKE N'%rød%'
                THEN N'Rød'
            WHEN web2.Name LIKE 'beige' OR web3.Name LIKE 'beige%' OR art.Name LIKE '%cream%' OR art.Name LIKE '%beige%'
                THEN N'Beige'
            WHEN web2.Name LIKE '%brun%' OR web3.Name LIKE 'brun%' OR art.Name LIKE '%brown%' OR
                 art.Name LIKE '%brun%' OR art.Name LIKE '%tan%' THEN N'Brun'
            WHEN web2.Name LIKE 'orange' OR web3.Name LIKE 'orange%' OR art.Name LIKE '%orange%' OR
                 art.Name LIKE N'%oransje%' THEN N'Oransje'
            WHEN web2.Name LIKE N'blå' OR web3.Name LIKE N'blå%' OR art.Name LIKE '%blue%' OR art.Name LIKE N'%blå%' OR
                 art.Name LIKE '%sky%' OR art.Name LIKE '%navy%' THEN N'Blå'
            WHEN web2.Name LIKE 'sort' OR web3.Name LIKE 'sort%' OR web2.Name LIKE 'svart%' OR
                 web3.Name LIKE 'svart%' OR art.Name LIKE '%black%' OR art.Name LIKE N'%sort%' OR
                 art.Name LIKE '%svart%' THEN N'Svart'
            WHEN web2.Name LIKE 'lilla%' OR web3.Name LIKE 'lilla%' OR art.Name LIKE '%purple%' OR
                 art.Name LIKE '%lilla%' THEN N'Lilla'
            WHEN web2.Name LIKE 'rosa' OR web3.Name LIKE '%Rosa%' OR art.Name LIKE '%pink%' OR art.Name LIKE N'%rosa%'
                THEN N'Rosa'
            WHEN web2.Name LIKE N'grå' OR web3.Name LIKE N'grå%' OR art.Name LIKE '%grey%' OR art.Name LIKE N'%grå%' OR
                 art.Name LIKE '%charcoal%' THEN N'Grå'
            WHEN web2.Name LIKE 'ensfarge%' THEN 'Ensfarget'
            END                                                                         AS 'product_color',

        CASE
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Anni Downs%' THEN 'Anni Downs'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Lynette Anderson%' THEN 'Lynette Anderson'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Jen Kingwell%' THEN 'Jen Kingwell'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Tula Pink%' THEN 'Tula Pink'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Kaffe Fassett%' THEN 'Free Spirit'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Tim Holtz%' THEN 'Tim Holtz'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Anna Maria Horner%' THEN 'Anna Maria Horner'
            WHEN COALESCE(web3.Name, web2.Name) LIKE 'Meags and Me%' THEN 'Meags and Me'
            END AS 'designer',

        CASE
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

            WHEN art.Name LIKE '%janome%' OR art.Name LIKE '%jabome%' OR art.Name Like '%Janbome%' OR
                 art.Name LIKE '%Jasbome%' THEN 'Janome'
            WHEN REPLACE(art.Name, ' ', '') LIKE '%baby lock%' OR web2.Name LIKE 'baby%lock%' THEN 'Baby Lock'
            WHEN art.Name LIKE '%brother%' THEN 'Brother'
            WHEN art.Name LIKE '%prym%' THEN 'Prym'
            WHEN sup.Name LIKE '%byannie%' THEN 'By Annie'
            WHEN sup.Name LIKE '%annaka%' THEN 'AnnAKa'
            WHEN art.Name LIKE '%guterman%' OR art.Name LIKE '%gutterman%' THEN N'Gütermann'
            WHEN art.Name LIKE '%Organ needle%' THEN 'Organ Needles'
            WHEN art.Name LIKE '%Avalana%' OR art.Name LIKE 'Nellies Shirtings%' OR art.Name LIKE 'Molly Roses%'
                THEN 'Stoffabrics'
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
            --ELSE sup.Name
            END                                                                         AS vendor,

        CASE WHEN CAST(CURRENT_TIMESTAMP - art.LastUpdate AS INT) < 90 THEN 'Nyhet' END AS new_tag

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
             LEFT JOIN Articles art_com ON art_com.ArticleID = com.MainArticleID
    WHERE (art.VisibleOnWeb = 1 AND NOT art.SellAsComponents = 1) -- Visible on web and not sell as components of a main product.
       OR (art.VisibleOnWeb = 0 AND art_com.ArticleID IS NOT NULL AND art.Picture IS NOT NULL AND
           CAST(ISNULL(rec.C, 0) - ISNULL(sol.C, 0) AS INT) > 0)
        OR art.Name LIKE '%brother%' OR art.Name LIKE '%baby%lock%' OR art.Name LIKE '%janome%'
)
SELECT pro.sku,
       source_id,
       source_updated,
       title,
       CASE
           WHEN price_unit LIKE 'meter' THEN ROUND(CAST(price AS FLOAT) / 10.0, 1)
           WHEN price IS NULL THEN 0
           ELSE price
           END                                                                                                     AS price,
       CASE
           WHEN price_unit LIKE 'meter' THEN 'desimeter'
           ELSE price_unit
           END                                                                                                     AS price_unit,
       CASE WHEN NOT available > 0 OR available IS NULL THEN 0 ELSE available END                                  AS available,
       --body_html,
       --images,
       ISNULL(product_type, 'Annet') AS product_type,
       product_subtype,
       product_subtype2,
       product_subtype3,
       product_color,
       vendor,
       designer,
       hide_when_empty,
       CASE
           WHEN discount_start < CURRENT_TIMESTAMP AND CURRENT_TIMESTAMP < discount_end AND discounted_price > 0
               THEN IIF(price_unit LIKE 'meter', ROUND(CAST(discounted_price AS FLOAT) / 10.0, 1), discounted_price) END                                                                           AS discounted_price,
       CONCAT(product_type, ',', product_subtype, ',', product_subtype2, ',', product_subtype3, ',', product_color, ',', vendor, ',', designer, ',',
              new_tag)                                                                                             AS tags

FROM Products pro
WHERE NOT (price < 5 AND available < 1) AND source_id NOT IN (51701, 55014, 55897)
ORDER BY source_id  -- or, order by source_updated ASC
;

-- Todo: Check status inactive vs. active in PCKasse...
