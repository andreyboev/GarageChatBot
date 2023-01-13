import emoji
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove, ChatMemberUpdated
from emoji import emojize

from db_controller import *
from utils import get_chart_activity_stat

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(text="Добро пожаловать!", reply_markup=ReplyKeyboardRemove())


@router.message(Command(commands=["menu"]))
async def cmd_menu(message: Message):
    main_menu = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='👨‍👩‍👧‍👦 Участники', callback_data='users_button_click')],
            [types.InlineKeyboardButton(text='📈 Статистика активности', callback_data='stat_button_click')],
            [types.InlineKeyboardButton(text='🎲 Играть в ...', callback_data='game_button_click')]])
    await message.answer(text="Выберите нужный пункт", reply_markup=main_menu)


@router.callback_query(Text(text='stat_button_click'))
async def stat_button_click(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    await call.message.delete()
    await call.message.answer_photo(photo=get_chart_activity_stat(chat_id))


@router.message(Command(commands=["help"]))
async def cmd_start(message: Message):
    await message.answer(text="Для обращения к боту, необходимо, чтобы запрос начинался со слова \"Бот\"\n"
                              "Фразы, на которые реагирует бот:\n"
                              "\"меня зовут\" - задать своё имя\n"
                              "\"кто я\" - узнать своё имя\n"
                              "\"кто болтушка\" - активность участников\n")


@router.chat_member()
async def members_process(event: ChatMemberUpdated, bot: Bot):
    if not has_chat(event.chat.id):
        add_chat(event.chat.id, event.chat.title)


def reg_user(chat_id, user_info):
    exist_user = has_user(chat_id, user_info.id)
    if not exist_user:
        username = user_info.username if user_info.username is not None else str(user_info.id)
        add_user(user_info.id, username, chat_id)


@router.message(F.photo)
async def photo_msg(message: Message):
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id)


@router.message(F.text.regexp(r'^(?!Бот).+$'))
async def cmd_msg(message: Message):
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id)


@router.message(Text(startswith='Бот'))
async def cmd_msg(message: Message):
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id)
    if 'меня зовут' in message.text.lower():
        text = message.text
        name_start = text.find('меня зовут') + 10
        update_user_name(message.from_user.id, text[name_start + 1:], message.chat.id)
        await message.answer(f'Привет, {text[name_start + 1:]}')
    if 'кто я' in message.text.lower():
        info = get_user_info(message.from_user.id, message.chat.id)
        await message.answer(f'Ты {info[2]}')
    if 'кто болтушка' in message.text.lower():
        user = max(get_users_msg_count(message.chat.id), key=lambda x: x[1])[0]
        await message.answer(f"Говорун: {user} {emojize(':monkey_face:')}")
