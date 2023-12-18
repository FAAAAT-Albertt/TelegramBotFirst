from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.types import ContentType
from text import CALLBACK_GET_CODE, CALLBACK_REG_CODE, START_TEXT
from config import TOKEN
import logging
import asyncio
import json
from get_total_price import get_response
from db import db_connect, table_clients_comp_price, table_clients_comp_product, fetchall_codes, workers_service
from table import check_unn, check_number
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from gen_code import generic_code

storage: MemoryStorage = MemoryStorage()
bot = Bot(token=TOKEN)
db = Dispatcher(bot, storage=storage)


class UseForm(StatesGroup):
    number = State()
    code = State()
    car_info = State()


inline_but1_getcode = InlineKeyboardButton(text="Загрузить чек", callback_data="total_price")
inline_but2_getcode = InlineKeyboardButton(text="Я купил без чека", callback_data="not_total_price")
inline_markup_getcode = InlineKeyboardMarkup(row_width=2).add(inline_but1_getcode).add(inline_but2_getcode)


inline_but1 = InlineKeyboardButton(text="Получить промокод", callback_data="getcode")
inline_but2 = InlineKeyboardButton(text="Выбрать СТО", url="https://www.youtube.com/")
inline_but3 = InlineKeyboardButton(text="Зарегистрировать промокод", callback_data="regcode")
inline_markup = InlineKeyboardMarkup(row_width=2).add(inline_but1).add(inline_but2).add(inline_but3)

inline_but_restart = InlineKeyboardButton(text="Вернуться в начало бота", callback_data="restart")
inline_markup_code = InlineKeyboardMarkup(row_width=2).add(inline_but2).add(inline_but_restart)

inline_but2_restart = InlineKeyboardButton(text="Вернуться в начало бота", callback_data="restart2")
inline_but_centre = InlineKeyboardButton(text="Запросить помощь", url="https://oil-t.ru/kontakty/?utm_source=ssilka&utm_medium=bot&utm_campaign=free_change")
inline_markup_centre = InlineKeyboardMarkup(row_width=2).add(inline_but_centre).add(inline_but2_restart)

but_contact = KeyboardButton(text="Отправить телефон", request_contact=True)
markup_contact = ReplyKeyboardMarkup(resize_keyboard=True).add(but_contact)

@db.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer(text=START_TEXT, reply_markup=inline_markup)


@db.callback_query_handler()
async def callback_button(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "getcode":
        return await callback.message.reply(text=CALLBACK_GET_CODE, reply_markup=inline_markup_getcode)
    elif callback.data == "regcode":
        await callback.message.answer(text=CALLBACK_REG_CODE, reply_markup=markup_contact)
        # await UseForm.number.set()
    elif callback.data == "total_price":
        return await callback.message.answer(text="Загрузите фотографии чека и продукции:")
    elif callback.data == "not_total_price":
        return await callback.message.answer(text="Загрузите пожалуйста фотографию чека или накладной")
    elif callback.data == "restart":
        return await callback.message.answer(text=START_TEXT, reply_markup=inline_markup)
    elif callback.data == "restart2":
        return await callback.message.answer(text=START_TEXT, reply_markup=inline_markup)

@db.message_handler(content_types=ContentType.PHOTO)
async def iter_photo(message: types. Message):
    await message.answer("⏳ Сейчас все проверим...")

    await message.photo[-1].download(destination_file=f'C:/Users/TOLSTIY/Desktop/check_bot/total_prices/{message.photo[-1].file_unique_id}-{message.from_user.id}.jpg')
    path_photo = f"C:/Users/TOLSTIY/Desktop/check_bot/total_prices/{message.photo[-1].file_unique_id}-{message.from_user.id}.jpg"

    i = get_response(path_photo)
    if i['code'] == 1:
        price = int(i['data']['json']['totalSum']) // 100
        unn = int(i['data']['json']['userInn'].strip())
        code = check_unn(unn, price)
        await message.answer(text=f"Ваш промокод на бесплатную замену масла - {code}. Промокод действует до 1 сентября 2023 года. Выберите СТО, которое участвует в акции и предъявите промокод его сотруднику.", reply_markup=inline_markup_code)

        user_id = message.from_user.id
        file_uniq = message.photo[-1].file_unique_id
        time = f"{message.date.day}-{message.date.month}-{message.date.year}, {message.date.hour}:{message.date.minute}:{message.date.second}"
        price_photo = path_photo
        unn_db = str(unn)
        name_bussines = i['data']['json']['user']
        adress = i['data']['json']['retailPlaceAddress']
        worker_name = i['data']['json']['operator']
        price_db = price
        code_db = code

        table_clients_comp_price(user_id, file_uniq, time, price_photo, unn_db, name_bussines, adress, worker_name, price_db, code_db)

    else:
        await message.answer("Я вас не понимаю.\nОтправьте фото чека.")
        user_id = message.from_user.id
        file_uniq = message.photo[-1].file_unique_id
        photo_prod = path_photo
        table_clients_comp_product(user_id, photo_prod, file_uniq)



@db.message_handler(content_types=ContentType.CONTACT)
async def mess_number(message: types.Message, state: FSMContext):
    # async with state.proxy() as data:
    contact = message.contact.phone_number
    if check_number(contact)  is True:
        await message.answer(f"Ваш промокод -> {generic_code()}")
        # await message.answer(text="Введите пожалуйста промокод")
        # await UseForm.code.set()
    else:
        await message.answer("Вы не авторизованы как СТО, участвующее в акции.\nСвяжитесь пожалуйста с региональным офисом Ойл Трейд.", reply_markup=inline_markup_centre)


@db.message_handler(state=UseForm.code)
async def mess_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['code'] = message.text
        for check_code in fetchall_codes():
            if check_code[0] == data['code']:
                await UseForm.next()
                await UseForm.car_info.set()
                return await message.answer("Введите пожалуйста марку и год выпуска автомобиля, в котором меняется масло.")
            else:
                return await message.answer(text="Вы не авторизованы как СТО, участвующее в акции.\nСвяжитесь пожалуйста с региональным офисом Ойл Трейд.", reply_markup=inline_markup_centre)


@db.message_handler(state=UseForm.car_info)
async def mess_carinfo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['car_info'] = message.text

        user_id = message.from_user.id
        username = message.from_user.username
        phone_numb = data['number']
        car_info = data['car_info']
        code = data['code']
        status_code = False
        time = f"{message.date.day}-{message.date.month}-{message.date.year}, {message.date.hour}:{message.date.minute}:{message.date.second}"
        await message.answer("Промокод погашен, оплата за замену будет произведена в рамках акции.")
        workers_service(user_id, phone_numb, code, status_code, time, car_info)
        await UseForm.next()



async def main():
    logging.basicConfig(level=logging.INFO)
    await db.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
