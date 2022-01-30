from minsymaskin.translate import DeepTranslator
from minsymaskin.translate.types import Language


def test_german_to_danish():
    german_text = """
    Einigkeit und Recht und Freiheit
    Für das deutsche Vaterland!
    Danach lasst uns alle streben
    Brüderlich mit Herz und Hand!
    Einigkeit und Recht und Freiheit
    Sind des Glückes Unterpfand;
    |: Blüh' im Glanze dieses Glückes,
    Blühe, deutsches Vaterland! :|
    """
    translator = DeepTranslator(language_from=Language.GERMAN, language_to=Language.DANISH)
    danish_text = translator.translate(text_to_translate=german_text)
    translator.quit()

    assert danish_text.strip().startswith("Enhed og retfærdighed og frihed")
    assert danish_text.strip().endswith("Er et løfte om lykke;")
