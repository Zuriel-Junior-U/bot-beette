import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods.delete_message import DeleteMessage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup
)

import dotenv


dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
form_router = Router()
dp = Dispatcher()
dp.include_router(form_router)


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text=f"Menu Principal", callback_data=f"menu")
    builder.button(text='Verificar ID', callback_data='verificar_id')
    builder.adjust(1, 1)
    await message.answer(text='Seja bem Vindo!', reply_markup=builder.as_markup())

async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
