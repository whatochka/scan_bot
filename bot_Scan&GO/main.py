import types

from data.import_lib import *
from data.text import *
from data import config
from data.keyboards import get_start_ikb, get_main_ikb, get_back_ikb, get_yes_or_no, get_languages, get_back_ikb_dict, \
    get_back, get_dict_ikb
from tools.photo_to_text.phpto_to_text import photo_to_text
from tools.photo_to_text.check_lang import check_lang
from tools.photo_to_text.languages import language_dict, language_dict_google
from tools.translator.translator import translator
from data.DataBase.db import BotDB
from googletrans import Translator

trans = Translator()

API = config.TOKEN

BotDB = BotDB("C:/Workplace/Новая папка/data/DataBase/botbd.db")

storage = MemoryStorage()
bot = Bot(API)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    photo = State()
    check_lang = State()
    translate_text = State()
    translate_mess = State()
    dictionary = State()
    add = State()
    dell = State()


async def on_startup(_):
    print("Запуск: успешно!")


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    lang = "ru"
    if not BotDB.user_exists(message.from_user.id, lang):
        BotDB.add_user(message.from_user.id, lang)

    await bot.send_sticker(chat_id=message.from_user.id,
                           sticker='CAACAgIAAxkBAAEJJztkdeHM50DbWXfluePFFNieDphdZwACmgwAAu-d2UupTUQhmiqreS8E')

    await bot.send_message(chat_id=message.from_user.id,
                           text=start,
                           reply_markup=get_start_ikb())
    await message.delete()


@dp.callback_query_handler(text='info')
async def info(callback: types.CallbackQuery):
    await callback.message.edit_text(text=about_bot,
                                     reply_markup=get_back())


@dp.callback_query_handler(text='main', state='*')
async def main(callback: types.CallbackQuery, state):
    await state.finish()

    await callback.message.edit_text(text=main_menu,
                                     reply_markup=get_main_ikb())


@dp.callback_query_handler(text='back')
async def back(callback: types.CallbackQuery):
    await callback.message.edit_text(text=start,
                                     reply_markup=get_start_ikb())


@dp.callback_query_handler(text='translator')
async def translate_text(callback: types.CallbackQuery):
    await callback.message.edit_text(text=translator_start,
                                     reply_markup=get_languages())

    await UserState.translate_mess.set()


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == 'lang', state=UserState.translate_mess)
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['lang'] = callback.data.split('_')[1]

    await callback.message.edit_text(text=translator_end)


@dp.message_handler(state=UserState.translate_mess)
async def translate_mess(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text

    if text.lower() != 'стоп':
        origin, text = await translator(text, data['lang'])
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'{origin} —> {text}')
        await message.delete()
    else:
        await state.finish()

        await message.delete()
        await bot.send_message(chat_id=message.from_user.id,
                               text='Нажмите кнопку, чтобы вернуться в главное меню!',
                               reply_markup=get_back_ikb())


@dp.callback_query_handler(text='scan')
async def scan_text(callback: types.CallbackQuery):
    await callback.message.edit_text(text=scan_start,
                                     reply_markup=get_back_ikb())

    await UserState.photo.set()


@dp.message_handler(content_types=['photo'], state=UserState.photo)
async def get_text(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    direction = 'C:/Workplace/Новая папка/media/photos'

    async with state.proxy() as data:
        if 'lang' in data:
            pass
        else:
            data['lang'] = None

    await bot.send_message(uid, f'Изображение обрабатывается...')
    await message.photo[-1].download(destination_file=f'{direction}/{uid}_photo.jpg')

    text = await photo_to_text(uid, data['lang'], direction)
    async with state.proxy() as data:
        data['text'] = text
        data['mes'] = message

    check_lang_text, lang, confidence = check_lang(text)

    if check_lang_text:
        await bot.send_message(chat_id=uid,
                               text=lang_choose_translate,
                               reply_markup=get_languages())
        await UserState.translate_text.set()
    else:
        await bot.send_message(chat_id=uid,
                               text=f'Кажется это {language_dict_google[lang]} язык. Совпадение: '
                                    f'{round(confidence, 3) * 100}%\n'
                                    f'Это действительно он?',
                               reply_markup=get_yes_or_no())

        await UserState.next()


@dp.callback_query_handler(text='no', state=UserState.check_lang)
async def choose_language(callback: types.CallbackQuery):
    await callback.message.edit_text(text=lang_choose,
                                     reply_markup=get_languages())


@dp.callback_query_handler(text='yes', state=UserState.check_lang)
async def choose_language_translate(callback: types.CallbackQuery):
    await callback.message.edit_text(text=lang_choose_translate,
                                     reply_markup=get_languages())
    await UserState.translate_text.set()


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == 'lang', state=UserState.check_lang)
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(lang=language_dict.get(callback.data.split('_')[1]))
    async with state.proxy() as data:
        data['state'] = state

    await get_text(data['mes'], data['state'])


@dp.callback_query_handler(lambda cb: cb.data.split('_')[0] == 'lang', state=UserState.translate_text)
async def translate_text(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = callback.data.split('_')[1]

    origin, text = await translator(data['text'], lang)

    await callback.message.edit_text(text=f'Результат:\n\n{text}',
                                     reply_markup=get_back_ikb())
    await state.finish()


@dp.callback_query_handler(text='user_dict', state='*')
async def add_records(callback: types.CallbackQuery):
    within_als = {
        "day": ('today', 'day', 'сегодня', 'день'),
        "month": ('month', 'месяц'),
        "year": ('year', 'год'),
    }

    cmd = ''
    within = 'year'

    if len(cmd):
        for k in within_als:
            for als in within_als[k]:
                if als == cmd:
                    within = k

    records = BotDB.add_records(callback.from_user.id, within)
    if len(records):
        answer = f"Словарь: \n\n"
        for r in records:
            answer += f"{r[2]} -> {trans.translate(r[2], 'ru').text}\n"

        await callback.message.edit_text(text=answer,
                                         reply_markup=get_back_ikb_dict())

    else:
        await callback.message.edit_text(text="Словарь пуст!",
                                         reply_markup=get_back_ikb_dict())
    await UserState.dictionary.set()


@dp.callback_query_handler(text='add_word', state=UserState.dictionary)
async def get_word(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Напишите слово, которое хотели бы добавить в словарь!',
                                     reply_markup=get_back_ikb())
    await UserState.add.set()


@dp.callback_query_handler(text='del_word', state=UserState.dictionary)
async def get_word(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Напишите слово, которое хотели бы удалить из словаря!',
                                     reply_markup=get_back_ikb())
    await UserState.dell.set()


@dp.message_handler(state=UserState.add)
async def add_word(message: types.Message, state: FSMContext):
    BotDB.add_record(message.from_user.id, message.text)

    await bot.send_message(chat_id=message.from_user.id,
                           text='Слово успешно добавлено в словарь!',
                           reply_markup=get_dict_ikb())

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 1)

    await message.delete()
    await state.finish()


@dp.message_handler(state=UserState.dell)
async def del_word(message: types.Message, state: FSMContext):
    BotDB.del_dict(message.from_user.id, message.text)

    await bot.send_message(chat_id=message.from_user.id,
                           text='Слово спешно удалено из словаря!',
                           reply_markup=get_dict_ikb())

    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id - 1)

    await message.delete()
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
