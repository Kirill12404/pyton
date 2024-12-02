from aiogram import types, Dispatcher, Bot
from aiogram.utils import executor
from credits import token
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlate_helper #ДОБАВИЛИ СЕГОДНЯ
import sqlite3
conn=sqlite3.connect('aqua.db')
cur=conn.cursor()
bot = Bot(token=token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

#sqlate_helper.add_slide('крутая', 12, 'самая крутая горка в аквапарке')



class HandleClient(StatesGroup):
   waiting_for_slide = State()
   waiting_for_name = State()
   waiting_for_number = State()


async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add('КУПИТЬ БИЛЕТ')
    cur.execute('SELECT name FROM slides')
    slides = cur.fetchall()
    for slide in slides:
        keyboard.add(slide[0])
    await message.answer('Добро пожаловать в аквапарк! Нажмите на название горки, чтобы получить больше информации, или на кнопку "купить билет", чтобы купить билет.', reply_markup=keyboard)
    await HandleClient.waiting_for_slide.set()
    

async def on_slide(message: types.Message):
    if message.text == 'КУПИТЬ БИЛЕТ':
        await message.answer('Стоимость билета - 2000 рублей на весь день. Чтобы купить билет, отправьте в чат своё имя:')
        await HandleClient.waiting_for_name.set()
    else:
        cur.execute('SELECT length, description FROM slides WHERE name = ?', [message.text])
        slide = cur.fetchone()
        await message.answer(f'{message.text} - {slide[1]}.\nПротяжённость горки - {slide[0]} метров.')


async def on_name(message: types.Message, state):
    await state.update_data(name=message.text)
    await message.answer('И номер телефона:')
    await HandleClient.waiting_for_number.set()


async def on_number(message: types.Message, state):
    await state.update_data(number=message.text)
    await message.answer('Спасибо! Менеджер свяжется с вами для оплаты заказа.')
    data = await state.get_data()
    number = data.get('number')
    name = data.get('name')
    try:

     sqlite_helper.add_reqests (name,number)

     admins = sqlite_helper.get_admins()

    except Exception as error:
        await message.answer(f'Ошибка добавления, {number} номер уже в базе данных')
    cur.execute('SELECT user_id FROM admins')
    admins = cur.fetchall()
    for admin in admins:
        await bot.send_message(admin[0], f'Новая заявка!\nИмя: {name},\nНомер: {number}')
    await HandleClient.waiting_for_slide.set()

async def admin(message: types.Message):
    try:
        password = message.text.split(' ')[1]
    except:
        await message.answer('Введите пароль')
    if password == '1234':
        try:
            sqlate_helper.add_admin(message.from_user.id)
            await message.answer('Теперь этот чат админский')
        except Exception as error:
            await message.answer('Вы уже админ')
    else: await message.answer('Неверный пароль')



def register_handlers(dp: Dispatcher):
   dp.register_message_handler(start, commands="start")
   dp.register_message_handler(admin, commands="admin")
   dp.register_message_handler(on_slide, state=HandleClient.waiting_for_slide)
   dp.register_message_handler(on_name, state=HandleClient.waiting_for_name)
   dp.register_message_handler(on_number, state=HandleClient.waiting_for_number)

register_handlers(dp)

executor.start_polling(dp, skip_updates=True)