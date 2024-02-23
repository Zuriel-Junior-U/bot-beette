import asyncio
import logging
import json
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
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)

import dotenv

import utils_db


dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
form_router = Router()
dp = Dispatcher()
dp.include_router(form_router)

class Form(StatesGroup):
    id_usuario = State()
    tipo_usuario = State()
    id_sala = State()

dados_salas = {
    'configuracoes': {
        'gales': 0,
        'start_horario': ['Desativado', ''],
        'stop_horario': ['Desativado', ''],
        'limite_wins': 1,
        'pular_pedra_win': 'Sim',
        'situacao': 'Desligado',
    },
    'estrategias': {
        'gatilhos': {
        },
        'padroes': {
        },
        'buscadores': {
        }
    }
        
}

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

async def menu_configuracoes(message: Message, id_telegram):
    usuario = utils_db.dados_usuario(id_telegram)
    builder = InlineKeyboardBuilder()
    if usuario['salas'] == {}:
        builder.button(text='➕ Cadastrar Sala', callback_data='cadastrar_sala')
        return await message.answer('Menu Configurações', reply_markup=builder.as_markup())
    
    builder.button(text='🔄 Situação: Desligado', callback_data='data')
    builder.button(text='🔄 Sala: 123', callback_data='data')
    builder.button(text='📖 Gatilhos', callback_data='data')
    builder.button(text='📖 Padrões', callback_data='data')
    builder.button(text='⏰ Start Horario', callback_data='data')
    builder.button(text='⏰ Stop Horario', callback_data='data')
    builder.button(text='✖️ Gales', callback_data='data')
    builder.button(text='⏹ LMT', callback_data='data')
    builder.button(text='🔄 PLP', callback_data='data')
    builder.button(text='➕ Cadastrar Sala', callback_data='cadastrar_sala')
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
    builder.button(text='➕ Cadastar Usuario', callback_data='cadastrar_usuario')
    builder.button(text='📖 Listar Usuarios', callback_data='listar_usuarios')
    builder.button(text='⬅️ Voltar', callback_data='menu_principal')
    builder.adjust(1, 1, 1)
    await message.answer(text='Menu Admistrativo', reply_markup=builder.as_markup())

async def cadastrar_usuario(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.id_usuario)
    await message.answer(
        "Informe o ID do usuario: "
    )

@form_router.message(Form.id_usuario)
async def process_cadastrar_usuario(message: Message, state: FSMContext) -> None:
    await state.update_data(id_telegram=message.text)
    await state.set_state(Form.tipo_usuario)
    await message.answer(
        f"Que tipo de usuario ele sera?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="cliente"),
                    KeyboardButton(text="adm"),
                ]
            ],
            resize_keyboard=True,
            reply_markup=None
        ),
    )

@form_router.message(Form.tipo_usuario)
async def final_cadastro_cliente(message: Message, state: FSMContext) -> None:
    await state.update_data(id_grup=message.text)
    data = await state.get_data()
    utils_db.cadastrar_usuario(data['id_telegram'], data['id_grup'])
    await state.clear()
    await message.answer(f"Usuário cadastrado como: {data['id_grup']}", 
                         reply_markup=ReplyKeyboardRemove())
    await menu_admistrativo(message)

async def listar_usuarios(message: Message):
    builder = InlineKeyboardBuilder()
    usuarios = utils_db.obter_usuarios()
    for usuario in usuarios:
        builder.button(text=f'{usuario[0]}', callback_data='data')
        builder.button(text='🗑', callback_data=f'deletar_usuario_{usuario[0]}')
        builder.adjust(2)
    builder.button(text='⬅️ Voltar', callback_data='meu_admistrativo')
    builder.adjust(1)
    await message.answer(text='Lista de Clientes', reply_markup=builder.as_markup())

async def cadastrar_sala(message: Message, state: FSMContext):
    await state.set_state(Form.id_sala)
    await message.answer(
        "Informe o ID da sala: "
    )

@form_router.message(Form.id_sala)
async def final_cadastro_sala(message: Message, state: FSMContext) -> None:
    await state.update_data(id_grup=message.text)
    data = await state.get_data()
    meu_id = message.from_user.id
    usuario = utils_db.dados_usuario(meu_id)
    usuario['sala_selecionada'] = data['id_grup']
    usuario['salas'][data['id_grup']] = dados_salas
    utils_db.atualizar_usuario(meu_id, 'dados_usuario', json.dumps(usuario))
    await state.clear()
    await menu_configuracoes(message, meu_id)

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
        await menu_configuracoes(message, meu_id)
    
    if call.data == 'meu_admistrativo' and usuario_liberado:
        await menu_admistrativo(message)
    
    if call.data == 'cadastrar_usuario' and usuario_liberado:
        await cadastrar_usuario(message, state)
    
    if call.data == 'listar_usuarios' and usuario_liberado:
        await listar_usuarios(message)
    
    if 'deletar_usuario_' in call.data:
        usuario = call.data.replace('deletar_usuario_', '')
        utils_db.deletar_usuario(usuario)
        await menu_admistrativo(message)
    
    if call.data == 'cadastrar_sala':
        await cadastrar_sala(message, state)

    if not usuario_liberado:
        await call.message.answer('usuario não cadastrado')
        await command_start(message, state)

async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
