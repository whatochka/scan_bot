from data.import_lib import *
from data.config import TESSERACT_PATH

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
pytesseract_cfg = r'--oem 3 --psm 6'


async def photo_to_text(uid, lang, direction):
    text = pytesseract.image_to_string(Image.open(f'{direction}/{uid}_photo.jpg'), lang=lang)
    Path(f'{direction}/{uid}_photo.jpg').unlink()

    return text
