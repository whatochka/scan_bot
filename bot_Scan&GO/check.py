import pytesseract
from PIL import Image
from googletrans import Translator
import re
from string import ascii_letters
from tools.photo_to_text.languages import language_dict_google, language_dict


# def lang_check(text) -> bool:
#     translator = Translator()
#     detect = translator.detect(text)
#
#     print(detect.confidence)
#
#     if detect.confidence == 1:
#         return True
#     else:
#         return False


pytesseract.pytesseract.tesseract_cmd = r'C:\Programs\Tesseract\tesseract.exe'

pytesseract_cfg = r'--oem 3 --psm 6'

image = Image.open('C:/Workplace/bot_Scan&GO/media/photos/test1.png')

lang = None
text = pytesseract.image_to_string(image, config=pytesseract_cfg, lang=lang)

translator = Translator()
detect = translator.detect(text)

print(language_dict.get(detect.lang))

print(detect)
print(text)

# if detect.confidence == 1:
#     pass
# else:
#     print(detect.lang, detect.confidence)
#     print(f'Это {language_dict_google.get(detect.lang)}?')
#
#     if input() == 'Нет':
#         text =


# for key, lang in language_dict.items():
#     if lang == langua:
#         image = Image.open('test.jpg')
#         text = pytesseract.image_to_string(image, config=pytesseract_cfg, lang=key)
#
#         if lang_check(text):
#             print(text)
#         else:
#             print(f'На фотографии не {key} язык')
#
#         break

# image = Image.open('test4.jpg')
# text = pytesseract.image_to_string(image, config=pytesseract_cfg)
#
# translator = Translator()
# print(translator.detect(text))
