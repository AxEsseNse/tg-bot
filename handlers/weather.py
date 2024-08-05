import aiohttp
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from ..constants import WEATHER_API_KEY, WEATHER_URL
from ..routers import weather_router
from ..states import WeatherForm


def get_wind_direct(deg: int) -> str:
    if not isinstance(deg, int):
        return 'Ошибка данных'

    if 0 <= deg < 22.5 or 337.5 <= deg <= 360:
        return 'Северный'
    elif deg < 67.5:
        return 'Северо-Восточный'
    elif deg < 112.5:
        return 'Восточный'
    elif deg < 157.5:
        return 'Юго-Восточный'
    elif deg < 202.5:
        return 'Южный'
    elif deg < 247.5:
        return 'Юго-Западный'
    elif deg < 292.5:
        return 'Западный'
    elif deg < 337.5:
        return 'Северо-Западный'
    else:
        return 'Ошибка данных'


async def get_weather(city_name) -> dict | None:
    async with aiohttp.ClientSession() as session:
        params = {
            'q': city_name,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru'
        }
        async with session.get(WEATHER_URL, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


@weather_router.message(Command('weather'))
async def command_weather(message: Message, state: FSMContext) -> None:
    await state.set_state(WeatherForm.city)
    await message.answer(
        'Введите город',
    )


@weather_router.message(WeatherForm.city)
async def weather_city(message: Message, state: FSMContext) -> None:
    city = message.text
    weather_data = await get_weather(city)
    if weather_data:
        answer = (
            f'Подробный прогноз погоды в городе <b>{city}</b>\n'
            f'  • Температура: <b>{weather_data["main"]["temp"]} °C</b> - '
            f'ощущается как <b>{weather_data["main"]["feels_like"]} °C</b>\n'
            f'  • Облачность: <b>{weather_data["weather"][0]["description"]}</b> '
            f'({weather_data["clouds"]["all"]}%)\n'
            f'  • Влажность: <b>{weather_data["main"]["humidity"]}%</b>\n'
            f'  • Ветер: <b>{get_wind_direct(weather_data["wind"]["deg"])} '
            f'{weather_data["wind"]["speed"]} м/с</b>\n'
            f'  • Атмосферное давление: <b>{weather_data["main"]["pressure"]} гПа</b>\n'
            f'  • Видимость: <b>{weather_data["visibility"]} м</b>'
        )
        await message.answer(answer, parse_mode='HTML')
        await state.clear()
    else:
        await message.answer('Ошибка получения данных с сервера. Возможно некорректно введен город')
