import asyncio
import random
import re

from aiogram import Router, Bot, F, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ChatMemberUpdated
from emoji import emojize

from controllers.db_controller import *
from controllers.geo_controller import check_city, get_city_info
from controllers.morpho_controller import create_rhyme
from states.cities_game_state import CitiesGameState
from utils import get_chart_activity_stat, get_right_bracket_word

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    await message.answer(text="Добро пожаловать!", reply_markup=ReplyKeyboardRemove())


@router.message(Text(startswith=':)'), F.from_user.username == 'korwart')
async def brackets_counter(message: Message):
    if not has_chat(message.chat.id):
        add_chat(message.chat.id, message.chat.title)
    reg_user(message.chat.id, message.from_user)
    current_value = message.text.count(')')
    count = inc_user_brackets_count(message.from_user.id, message.chat.id, current_value)
    await message.answer(f'В этот раз вы потратили {current_value} {get_right_bracket_word(current_value)}. '
                         f'А ВСЕГО {count} {get_right_bracket_word(count).upper()}! 😡🤬')


@router.message(Command(commands=["menu"]))
async def cmd_menu(message: Message):
    main_menu = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='👨‍👩‍👧‍👦 Участники', callback_data='users_button_click')],
            [types.InlineKeyboardButton(text='📈 Статистика активности', callback_data='stat_button_click')],
            [types.InlineKeyboardButton(text='🌇 Города', callback_data='game_cities_button_click')]
        ])
    await message.answer(text="Выберите нужный пункт", reply_markup=main_menu)


@router.callback_query(Text(text='stat_button_click'))
async def stat_button_click(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    await call.message.delete()
    await call.message.answer_photo(photo=get_chart_activity_stat(chat_id))


@router.callback_query(Text(text='users_button_click'))
async def game_button_click(call: types.CallbackQuery):
    personages = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐻‍❄️', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸',
                  '🐵', '🐔', '🐺', '🦆', '🦅', '🐗', '🐴', '🦄', '🐝', '🐛', '🐌', '🪱', '🐞', '🪰', '🪲', '🪳',
                  '🦟', '🦂', '🐢', '🐍', '🐙', '🦀', '🐠', '🐬', '🐅', '🐆', '🦓', '🦍', '🦧', '🦣', '🦛', '🐖',
                  '🐏', '🐑', '🦢', '🐕‍🦺', '🐈', '🐈‍⬛', '🐓', '🦝', '🦨', '🦔', '🦡', '🐀', '🐿', '🐁', '🦥', '🦦',
                  '🦫']
    users = get_users(call.message.chat.id)
    str = ''
    for user in users:
        str += f'{random.choice(personages)} {user}\n'
    await call.message.answer(str)


@router.callback_query(Text(text='game_cities_button_click'))
async def game_button_click(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Введите название любого города', reply_markup=
    types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text='Завершить'), types.KeyboardButton(text='Инфо о городе')]], resize_keyboard=True))
    await call.answer()
    await state.set_state(CitiesGameState.city)


# TODO: Промежуточные результаты.
# TODO: Время на ответ.
# TODO: Хранить не название города, а объект???
@router.message(CitiesGameState.city)
async def enter_city_state(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'Завершить':
        await message.answer('Конец игры', reply_markup=types.ReplyKeyboardRemove())
        if 'city' in data and len(data['city']['users_cities']) > 0:
            str = ''
            for user, count in data['city']['users_cities'].items():
                str += f'{get_user_info(user, message.chat.id)[2]}  {count}\n'
            await message.answer(f'Результаты:\n{str}')
        await state.clear()
        return
    if message.text == 'Инфо о городе':
        if 'city' in data:
            info = get_city_info(data["city"]["city"])
            await message.answer(info.address)
            return
    current_city = message.text.strip().lower()
    if not check_city(current_city):
        await message.answer(f'Такого города нет!\n')
        if 'city' in data:
            await message.answer(f'Введите город на букву \'{data["city"]["city"][-1].upper()}\'')
        return
    current_city = current_city.replace('ь', '').replace('й', 'и').replace('ы', '')
    if 'city' in data:
        old_city = data['city']['city']
        if data['city']['user'] == message.from_user.id:
            await message.answer(f'Не надо играть самому с собой, лучше подрочи!')
            return
        if old_city[-1] != current_city[0]:
            await message.answer(f'Неправильно, повторите ввод города на букву \'{old_city[-1].upper()}\'')
            return
        if current_city in data['city']['cities']:
            await message.answer(f'Неправильно, такой город уже был\nВведите название города на букву \'{old_city[-1].upper()}\'')
            return
        else:
            await message.answer(f'Верно, идём далее\nВведите название города на букву \'{current_city[-1].upper()}\'')
            users_cities = data['city']['users_cities']
            if message.from_user.id in users_cities:
                users_cities[message.from_user.id] += 1
            else:
                users_cities[message.from_user.id] = 1
            await state.update_data(city={
                'city': current_city,
                'user': message.from_user.id,
                'cities': [*data['city']['cities'], current_city],
                'users_cities': users_cities
            })

    else:
        await state.update_data(city={
            'city': current_city,
            'user': message.from_user.id,
            'cities': [current_city],
            'users_cities': {}
        })
        await message.answer(f'Введите название города на букву \'{current_city[-1].upper()}\'')


@router.message(Command(commands=["help"]))
async def cmd_start(message: Message):
    await message.answer(text="Для обращения к боту, необходимо, чтобы запрос начинался со слова \"Бот\"\n"
                              "Фразы, на которые реагирует бот:\n"
                              "\"меня зовут\" - задать своё имя\n"
                              "\"кто я\" - узнать своё имя\n"
                              "\"кто болтушка\" - активность участников\n"
                              "\"обзови\" - обзывает кого угодно\n"
                              "\"рифмуй\" - рифмует слова по правилам Алексея Николаевича\n")


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
    if not has_chat(message.chat.id):
        add_chat(message.chat.id, message.chat.title)
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id, len(message.text.split()))


@router.message(F.text.regexp(r'^(?!Бот).+$'), StateFilter(None))
async def cmd_msg(message: Message):
    if not has_chat(message.chat.id):
        add_chat(message.chat.id, message.chat.title)
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id, len(message.text.split()))


@router.message(Text(startswith='Бот'))
async def cmd_msg(message: Message):
    if not has_chat(message.chat.id):
        add_chat(message.chat.id, message.chat.title)
    reg_user(message.chat.id, message.from_user)
    inc_user_msg_count(message.from_user.id, message.chat.id, len(message.text.split()))
    if 'меня зовут' in message.text.lower():
        text = message.text
        name_start = text.find('меня зовут') + 10
        name = text[name_start + 1:].strip()
        pattern = re.compile("[@#]")
        if len(pattern.findall(name)) > 0 or len(name.strip()) == 0:
            await message.answer(f'Имя содержит недопустимые символы')
            return
        update_user_name(message.from_user.id, name, message.chat.id)
        await message.answer(f'Привет, {text[name_start + 1:]}')
        return
    if 'кто я' in message.text.lower():
        info = get_user_info(message.from_user.id, message.chat.id)
        await message.answer(f'Ты {info[2]}')
        return
    if 'кто болтушка' in message.text.lower():
        user = max(get_users_msg_count(message.chat.id), key=lambda x: x[1])[0]
        await message.answer(f"Говорун: {user} {emojize(':monkey_face:')}")
        return
    if 'обзови' in message.text.lower():
        text = message.text
        name = text[text.find('обзови') + 6:].strip()
        await message.answer(f'{name} {get_next_obscene_phrase(message.chat.id)}')
        return
    if 'рифмуй' in message.text.lower():
        text = message.text.lower()
        word = text[text.find('рифмуй') + 6:].strip()
        await message.answer(f'{create_rhyme(word)}')
        return
