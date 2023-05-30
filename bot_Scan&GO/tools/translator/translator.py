from data.import_lib import *


async def translator(text, lang):
    trans = Translator()
    result = trans.translate(text=text, dest=lang)

    return result.origin, result.text
