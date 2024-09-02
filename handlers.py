from aiogram import types
from aiogram.dispatcher import Dispatcher
from pdf_processing import process_pdf
import os


# Обработчик команды /start
async def send_welcome(message: types.Message):
    await message.reply("Привет! \n Жду файл .Pdf")


# Обработчик команды /help
async def send_help(message: types.Message):
    await message.answer("Бот переименовывает платежки в формате .Pdf")


# Обработчик команды /phone
async def send_phone(message: types.Message):
    await message.answer("Телефон: +7 (000) 000-00-00")


# Обработчик для получения и обработки PDF-файлов
async def handle_document(message: types.Message):
    document = message.document
    file_name = document.file_name
    await message.reply(f"{message.from_user.full_name}, у Вас имя файла: {file_name}")

    if 'pdf' in document.file_name.lower():  # Проверка, что файл - PDF
        file_path = await document.download(destination_dir=".")  # Загружаем документ
        processed_file_name = process_pdf(file_path.name)  # Обработка файла

        await message.reply(f"Файл был переименован в: {processed_file_name}")
        await message.answer_document(types.InputFile(processed_file_name))  # Отправка обработанного файла

        # Удаление временных файлов
        os.remove(processed_file_name)
    else:
        await message.reply("Пожалуйста, отправьте файл в формате '.pdf'")


# Функция для регистрации обработчиков
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(send_help, commands="help")
    dp.register_message_handler(send_phone, commands=["phone"])
    dp.register_message_handler(handle_document, content_types=types.ContentType.DOCUMENT)