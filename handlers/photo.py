import os
import tempfile

from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image

from ..routers import photo_router
from ..states import PhotoForm


def create_temp_directory():
    """Функция создания временной директории."""
    temp_dir = tempfile.mkdtemp()
    return temp_dir


@photo_router.message(Command('photo'))
async def command_photo(message: Message, state: FSMContext) -> None:
    await state.set_state(PhotoForm.photo)
    await message.answer('Отправьте фото для получения его разрешения')


@photo_router.message(PhotoForm.photo, F.document)
async def photo_form_photo(message: Message, state: FSMContext, bot: Bot):
    doc = message.document
    if doc.mime_type.startswith('image/'):
        file_info = await bot.get_file(doc.file_id)
        file_path = file_info.file_path

        downloaded_file = await bot.download_file(file_path)
        temp_dir = create_temp_directory()
        temp_filepath = '{temp_dir}/temp_image.jpg'.format(temp_dir=temp_dir)

        with open(temp_filepath, 'wb') as file:
            file.write(downloaded_file.getvalue())

        with Image.open(temp_filepath) as img:
            width, height = img.size

        os.remove(temp_filepath)
        await state.clear()
        await message.answer('Разрешение изображения: {width} x {height}'.format(width=width, height=height))
    else:
        await message.reply("Недопустимый тип файла. Пожалуйста, отправьте изображение.")


@photo_router.message(PhotoForm.photo, F.photo)
async def photo_form_incorrect_photo(message: Message):
    await message.answer('Необходимо отправлять изображение без сжатия')


@photo_router.message(PhotoForm.photo, ~F.photo)
async def photo_form_incorrect_filetype(message: Message):
    await message.answer('Недопустимый формат. Необходимо отправить изображение')
