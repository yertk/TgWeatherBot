from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import TOKEN, API_TOKEN_Weather
import requests

bot = Bot(TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True,
                         one_time_keyboard=True) # !!one-time... прячет клавиатуру после нажатия

b1 = KeyboardButton('/help')
b3 = KeyboardButton('/photo')
b4 = KeyboardButton('/weather')

HELP_COMMAND = """
<b>/help</b> - <em>список команд</em>
<b>/start</b> - <em>старт бота</em>
<b>/photo</b> - <em> прислать фото кота</em>
<b>/weather</b> - <em> погода в Питере

"""


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, text=HELP_COMMAND,
                           parse_mode='HTML')  # reply_markup=ReplyKeyboardRemove()) После /start убирает кнопки


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Добро Пожаловать!',
                           parse_mode="HTML",
                           reply_markup=kb)



@dp.message_handler(commands=['photo'])
async def photo_command(message: types.Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=' ') # html-address


@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    lat = 59.93909  # широта СПБ
    lon = 30.315831  # долгота СПБ


    # Задаем параметры запроса
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru_RU',  # язык ответа
        'limit': 7,  # срок прогноза в днях
        'hours': True,  # наличие почасового прогноза
        'extra': False  # подробный прогноз осадков
    }

    # Задаем значение ключа API
    api_key = API_TOKEN_Weather

    # Задаем URL API
    url = 'https://api.weather.yandex.ru/v2/forecast'

    # Делаем запрос к API
    response = requests.get(url, params=params, headers={'X-Yandex-API-Key': api_key})

    # Проверяем статус ответа
    if response.status_code == 200:
        # Преобразуем ответ в JSON формат
        data = response.json()
        # Выводим данные о текущей погоде
        await message.reply(f'Температура воздуха: {data["fact"]["temp"]} °C\n'
        f'Ощущается как: {data["fact"]["feels_like"]} °C\n'
        f'Скорость ветра: {data["fact"]["wind_speed"]} м/с\n'
        f'Давление: {data["fact"]["pressure_mm"]} мм рт. ст.\n'
        f'Влажность: {data["fact"]["humidity"]} %\n'
        f'Погодное описание: {data["fact"]["condition"]}\n')
    else:
        # Выводим код ошибки
        await message.reply(f'\U00002628Ошибка: {response.status_code}\U00002628')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
