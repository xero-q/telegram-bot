from deep_translator import GoogleTranslator


def translate_es_ru(text:str) -> str:
    """
    Returns the text translate from Spanish into Russian

    Args
        text (str): The text to be translated
    """

    translator = GoogleTranslator(source='es', target='ru')

    # Translate from English to Spanish
    translated = translator.translate(text)

    return translated

