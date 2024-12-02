import types, Dispatcher, Bot
import executor 
import sqlite3
import aiogram 
import helper


token='7002434588:AAH_ehQ2E9-A51hUSWWxYFi1e_MoMIdrOFQ'

bot = Bot(token=token,parse_mode='HTML')

dp=Dispatcher(bot, storage=MemoryStorage())

class UserQuiz(StateGroup):
    user_a1=State()
    user_a2=State()
    user_a3=State()
    user_a4=State()
    user_a5=State()

async def start(message: types.Message):
    await message.answer('Добро пожаловать в AE! Сыграйте в мини-игру, чтобы получить промокод. В чат придёт уведомление, как только раунд начнётся!')
    save_user(message.chat.id, 0)

    
async def game (message: types.Message,state):
    if message.text == 'НАЧАТЬ ИГРУ':
    question = get_all_questions()[0]
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(question[2], question[3])
    keyboard.add(question[4], question[5])
    await message.answer(f'Вопрос №1. {question[1]}', reply_markup=keyboard)
    await UsersQuiz.user_a1.set()
    await state.update_data(correct=question[6])
    await state.update_data(points=0)

async def stopgame (message: types.Message):
    if message.text == 'ОСТАНОВИТЬ ИГРУ':

        async def on_user_a1(message: types.Message, state):
    question = get_all_questions()[1]
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(question[2], question[3])
    keyboard.add(question[4], question[5])
    data = await state.get_data()
    if data.get('correct') == message.text:
        points = data.get('points') + 1
        await state.update_data(points=points)
    await message.answer(f'Вопрос №2. {question[1]}', reply_markup=keyboard)
    await UsersQuiz.user_a2.set()
    await state.update_data(correct=question[6])

async def start (message: types.Message):
    if message.text == 'СТАРТ'

async def close (message: types.Message):
    if message.text == 'ЗАКРЫТЬ ИГРУ'

def register_handlers(dp: Dispatcher):
   dp.register_message_handler(start, commands="start", state="*")
   dp.register_message_handler(game, commands="game", state="*")
   dp.register_message_handler(on_user_a1, state=UsersQuiz.user_a1)
   dp.register_message_handler(on_user_a2, state=UsersQuiz.user_a2)
   dp.register_message_handler(on_user_a3, state=UsersQuiz.user_a3)
   dp.register_message_handler(on_user_a4, state=UsersQuiz.user_a4)
   dp.register_message_handler(on_user_a5, state=UsersQuiz.user_a5)

    
reg(dp)

executor.start_polling(dp,skip_update=True)