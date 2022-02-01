from myshopify.translate import GoogleTranslator
from myshopify.translate.types import Language


def test_danish_to_norwegian():
    danish_text_to_translate = """
Enhed og retfærdighed og frihed
For det tyske fædreland!
Lad os alle stræbe efter dette
Broderlig med hjerte og hånd!
Enhed og retfærdighed og frihed
Er et løfte om lykke;
    """

    translator = GoogleTranslator(language_from=Language.DANISH, language_to=Language.NORWEGIAN)
    norwegian_text = translator.translate(text_to_translate=danish_text_to_translate)
    translator.quit()

    assert norwegian_text.strip().startswith("Enhet og rettferdighet og frihet")
    assert norwegian_text.strip().endswith("Er et løfte om lykke;")
