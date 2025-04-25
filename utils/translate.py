from deep_translator import GoogleTranslator


def translate_text(text: str, source: str, target: str) -> str:
    """
    Returns the text translate from source to target language

    Args
        text (str): The text to be translated
        source (str): The source language code
        target (str): The target language code
    Returns
        str: The translated text
    Raises
        Exception: If the translation fails
    Example
        translate_text('Hola', 'es', 'ru')
        # Output: 'Привет'
    """
    try:
        translator = GoogleTranslator(source=source, target=target)

        # Translate from Spanish into Russian
        translated = translator.translate(text)

        return translated
    except:
        raise Exception('Impossible to translate the desired text')
