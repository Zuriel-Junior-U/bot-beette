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

import utils_db


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

async def menu_principal(message: Message, id_telegram):
    usuario = utils_db.dados_usuario(id_telegram)
    builder = InlineKeyboardBuilder()
    builder.button(text='⚙️ Configurações', callback_data='menu_configuracoes')
    builder.button(text='🆘 Suporte', callback_data='data')
    builder.adjust(2)
    if usuario['tipo_usuario'] == 'adm':
        builder.button(text='👮‍♀️ Administrador', callback_data='meu_admistrativo')
        builder.adjust(2, 1)
    await message.answer(text='Menu Principal', reply_markup=builder.as_markup())

async def menu_configuracoes(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='🔄 Situação: Desligado', callback_data='data')
    builder.button(text='🔄 Sala: 123', callback_data='data')
    builder.button(text='📖 Gatilhos', callback_data='data')
    builder.button(text='📖 Padrões', callback_data='data')
    builder.button(text='⏰ Start Horario', callback_data='data')
    builder.button(text='⏰ Stop Horario', callback_data='data')
    builder.button(text='✖️ Gales', callback_data='data')
    builder.button(text='⏹ LMT', callback_data='data')
    builder.button(text='🔄 PLP', callback_data='data')
    builder.button(text='➕ Cadastrar Sala', callback_data='data')
    builder.button(text='⬅️ Voltar', callback_data='menu_principal')
    builder.adjust(2, 2, 2, 2, 2, 1)
    await message.answer(text='Menu Configurações', reply_markup=builder.as_markup())

async def verificar_usuario(id_telegram):
    usuarios = utils_db.obter_usuarios()
    if str(id_telegram) in str(usuarios):
        return True
    return False

async def menu_admistrativo(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text='➕ Cadastar Usuario', callback_data='data')
    builder.button(text='📖 Listar Usuarios', callback_data='data')
    builder.button(text='⬅️ Voltar', callback_data='menu_principal')
    builder.adjust(1, 1, 1)
    await message.answer(text='Menu Admistrativo', reply_markup=builder.as_markup())

@form_router.callback_query()
async def my_call(call: types.CallbackQuery, state: FSMContext):
    meu_id = call.from_user.id
    message = call.message
    usuario_liberado = await verificar_usuario(meu_id)
    await call.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if call.data == 'verificar_id':
        await call.message.answer(f'ID: {meu_id}')
        await command_start(message, state)
    if call.data == 'menu_principal' and usuario_liberado:
        await menu_principal(message, meu_id)

    if call.data == 'menu_configuracoes' and usuario_liberado:
        await menu_configuracoes(message)
    
    if call.data == 'meu_admistrativo' and usuario_liberado:
        await menu_admistrativo(message)
    
    if not usuario_liberado:
        await call.message.answer('usuario não cadastrado')
        await command_start(message, state)

async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
