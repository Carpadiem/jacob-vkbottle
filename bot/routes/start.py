# imports
from vkbottle.bot import BotLabeler, Message
from fuzzywuzzy import fuzz
from keyboards import keyboards
from .help import game_commands

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# handlers
@bl.message(text='начать')
async def start(m: Message):    
    text = f'Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards.get('start')
    await m.answer(message=text, keyboard=keyboard)

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
        if percent >= 60: # 50 - процент совпадения похожих фраз
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