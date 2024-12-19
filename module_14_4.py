from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_info = KeyboardButton(text="Информация")
button_chet = KeyboardButton(text="Рассчитать")
button_buy = KeyboardButton(text="Купить")
kb.row(button_chet, button_info, button_buy)

inlkb = InlineKeyboardMarkup()
inbutton_schet = InlineKeyboardButton(text="Рассчитать норму калорий",  callback_data="calories")
inbutton_formula = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
inlkb.row(inbutton_formula, inbutton_schet)

inlnkb_buy = InlineKeyboardMarkup()
product1_but = InlineKeyboardButton(text="Product1", callback_data="product_buying")
product2_but = InlineKeyboardButton(text="Product2", callback_data="product_buying")
product3_but = InlineKeyboardButton(text="Product3", callback_data="product_buying")
product4_but = InlineKeyboardButton(text="Product4", callback_data="product_buying")
inlnkb_buy.row(product1_but, product2_but, product3_but, product4_but)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()

@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=inlkb)

@dp.message_handler(text = "Купить")
async def get_buying_list(message):
    for numb in range(1, 5):
        req_for_db = crud_functions.get_all_products(numb)
        text_for_answer = f"Название: {req_for_db[0]} | Описание: {req_for_db[1]} | Цена: {req_for_db[-1]}"
        with open(f"./image/picture{numb}.jpg", "rb") as img:
            await message.answer_photo(img, text_for_answer)
    await message.answer("Выберите продукт для покупки:", reply_markup=inlnkb_buy)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text="Информация")
async def get_info(message):
    await message.answer("Привет!, я бот помогающий твоему здоровью, при нажатии кнопки 'Расчитать', "
                         "расчитаю норму калорий за сутки")

@dp.message_handler(commands=["start"])
async def start(message):
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calorie = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
    await message.answer(f"Ваша норма калорий {calorie}")
    await state.finish()

@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)