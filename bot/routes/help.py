# imports
from vkbottle.bot import BotLabeler, Message
from fuzzywuzzy import fuzz
from emojies import emojies
from rules import PayloadContainsOrTextRule

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# variables
game_commands = {
    # category
    'general': {
        'category_text': 'Основные',
        'category_emoji': emojies.ledger,
        'category_commands': [
            { 'command_text': 'Профиль', 'command_emoji': emojies.ledger },
            { 'command_text': 'Деньги', 'command_emoji': emojies.dollar_banknote },
            { 'command_text': 'Ресурсы', 'command_emoji': emojies.wood },
            { 'command_text': 'Энергия', 'command_emoji': emojies.high_voltage },
            { 'command_text': 'Банк', 'command_emoji': emojies.bank },
            { 'command_text': 'Бизнес', 'command_emoji': emojies.briefcase },
            { 'command_text': 'Опыт/Уровень', 'command_emoji': emojies.trophy },
            { 'command_text': 'Работа', 'command_emoji': emojies.desktop },
            { 'command_text': 'Инвентарь', 'command_emoji': emojies.backpack },
            { 'command_text': 'Питомец', 'command_emoji': emojies.fox },
            { 'command_text': 'Кейсы', 'command_emoji': emojies.package },
            { 'command_text': 'Достижения', 'command_emoji': emojies.trophy },
        ]
    },
    # category
    'games': {
        'category_text': 'Игры',
        'category_emoji': emojies.cube,
        'category_commands': [
            { 'command_text': 'Кубик', 'command_emoji': emojies.cube },
            { 'command_text': 'Стакан', 'command_emoji': emojies.cup },
            { 'command_text': 'Казино', 'command_emoji': emojies.slot_machine },
        ]
    },
    # category
    'other': {
        'category_text': 'Другое',
        'category_emoji': emojies.mount,
        'category_commands': [
            { 'command_text': 'Пикча', 'command_emoji': emojies.mount },
            { 'command_text': 'Реф (реферальная система)', 'command_emoji': emojies.ballot_box },
            { 'command_text': 'Промо', 'command_emoji': emojies.red_envelope },
            { 'command_text': 'Донат', 'command_emoji': emojies.gem_stone },
            { 'command_text': 'Репорт', 'command_emoji': emojies.red_triangle },
            { 'command_text': 'Паспорт', 'command_emoji': emojies.identification_card },
            { 'command_text': 'Тоталы', 'command_emoji': emojies.printer },
        ]
    },
    # category
    'mtaresources': {
        'category_text': 'MTA',
        'category_emoji': emojies.video_game,
        'category_commands': [
            { 'command_text': 'mtaevent', 'command_emoji': emojies.video_game },
            { 'command_text': 'supermta', 'command_emoji': emojies.video_game },
            { 'command_text': 'mtareceived', 'command_emoji': emojies.scroll },
        ]
    },
    # category
    'pockets': {
        'category_text': 'Карманы',
        'category_emoji': emojies.phone,
        'category_commands': [
            { 'command_text': 'Телефон', 'command_emoji': emojies.phone },
            { 'command_text': 'Лептоп', 'command_emoji': emojies.laptop },
        ]
    },
}

# handlers

@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_help' }, text='помощь'))
async def help(m: Message):    
    answer_text = f'Список команд в игре:\n\n'
    for category, value in game_commands.items():
        category_text: str = value['category_text']
        category_emoji: str = value['category_emoji']
        category_commands: list = value['category_commands']
        answer_text += f'{category_emoji} {category_text}\n'
        for command in category_commands:
            command_emoji = command['command_emoji']
            answer_text += f'⠀⠀{command_emoji} {command["command_text"]}\n'
        answer_text += '\n'
    await m.answer(message=answer_text)


@bl.message()
async def unknown_message(m: Message):
    input_text = m.text
    matches = []
    # получение текстов игровых команд
    text_selections: list = []
    for category, value in game_commands.items():
        category_commands = value['category_commands']
        for command in category_commands:
            command_text = command['command_text']
            text_selections.append(command_text)
    # поиск похожих слов
    for text in text_selections:
        percent = fuzz.WRatio(input_text, text)
        if percent >= 60: # 60 - процент совпадения похожих фраз
            matches.append(text)
    # если похожие слова есть
    if len(matches) > 0:
        answer_text = f'Такой команды нет. Возможно, вы имели в виду:\n\n'
        for match in range(len(matches)):
            answer_text += f'{matches[match]}\n'
        answer_text += f'\n\nВведите "помощь", чтобы получить список доступных команд'
        await m.answer(answer_text)
    else:
        answer_text = 'Такой команды нет\nВведите "помощь", чтобы получить список доступных команд.'
        await m.answer(answer_text)