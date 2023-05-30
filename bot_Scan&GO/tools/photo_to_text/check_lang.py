from googletrans import Translator


def check_lang(text):
    translator = Translator()
    detect = translator.detect(text)

    lang = detect.lang
    confidence = detect.confidence

    if confidence == 1:
        return True, lang, confidence
    else:
        return False, lang, confidence
