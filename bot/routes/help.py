# imports
from vkbottle.bot import BotLabeler, Message
from keyboards import keyboards

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# variables
game_commands = {
    # category
    'general': {
        'category_text': 'Основные',
        'category_commands': [
            { 'command_text': 'Профиль' },
            { 'command_text': 'Деньги' },
            { 'command_text': 'Ресурсы' },
            { 'command_text': 'Энергия' },
            { 'command_text': 'Банк' },
            { 'command_text': 'Бизнес' },
            { 'command_text': 'Опыт/Уровень' },
            { 'command_text': 'Работа' },
            { 'command_text': 'Инвентарь' },
            { 'command_text': 'Питомец' },
            { 'command_text': 'Кейсы' },
            { 'command_text': 'Достижения' },
        ]
    },
    # category
    'games': {
        'category_text': 'Игры',
        'category_commands': [
            { 'command_text': 'Кубик', },
            { 'command_text': 'Стакан', },
            { 'command_text': 'Казино', },
        ]
    },
    # category
    'other': {
        'category_text': 'Другое',
        'category_commands': [
            { 'command_text': 'Пикча', },
            { 'command_text': 'Реф (реферальная система)' },
            { 'command_text': 'Промо', },
            { 'command_text': 'Донат', },
            { 'command_text': 'Репорт', },
            { 'command_text': 'Паспорт', },
            { 'command_text': 'Тоталы', },
        ]
    },
    # category
    'mtaresources': {
        'category_text': 'MTA',
        'category_commands': [
            { 'command_text': 'mtaevent', },
            { 'command_text': 'supermta', },
            { 'command_text': 'mtareceived', },
        ]
    },
    # category
    'pockets': {
        'category_text': 'Карманы',
        'category_commands': [
            { 'command_text': 'Телефон', },
            { 'command_text': 'Лептоп', },
        ]
    },
}


# handlers
@bl.message(text='помощь')
async def help(m: Message):    
    answer_text = f'Список команд в игре:\n\n'

    for category, value in game_commands.items():
        category_text: str = value['category_text']
        category_commands: list = value['category_commands']
        answer_text += category_text + '\n'
        for command in category_commands:
            answer_text += f'⠀⠀{command["command_text"]}\n'
        answer_text += '\n'

    await m.answer(message=answer_text)
