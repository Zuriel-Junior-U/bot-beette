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
    builder.button(text=f"Menu Principal", callback_data=f"menu_principal")
    builder.button(text='Verificar ID', callback_data='verificar_id')
    builder.adjust(1, 1)
    await message.answer(text='Seja bem Vindo!', reply_markup=builder.as_markup())

async def menu_principal(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='⚙️ Configurações', callback_data='data')
    builder.button(text='🆘 Suporte', callback_data='data')
    builder.adjust(2)
    await message.answer(text='Menu Principal', reply_markup=builder.as_markup())

@form_router.callback_query()
async def my_call(call: types.CallbackQuery, state: FSMContext):
    meu_id = call.from_user.id
    message = call.message
    await call.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if call.data == 'verificar_id':
        await call.message.answer(f'ID: {meu_id}')
        await command_start(message, state)
    if call.data == 'menu_principal':
        await menu_principal(message)

async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
