from deep_translator import GoogleTranslator


def translate_es_ru(text:str) -> str:
    """
    Returns the text translate from Spanish into Russian

    Args
        text (str): The text to be translated
    """

    try:
        translator = GoogleTranslator(source='es', target='ru')

        # Translate from Spanish into Russian
        translated = translator.translate(text)

        return translated
    except:
        raise Exception('Impossible to translate the desired text')

