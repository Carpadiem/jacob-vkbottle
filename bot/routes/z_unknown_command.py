# imports
from vkbottle.bot import BotLabeler, Message
from fuzzywuzzy import fuzz
from emojies import emojies
from .general.help import game_commands
from database.entities import PlayerEntity
from database.repository import Repository

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message()
async def unknown_message(m: Message):
    # user from repo
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
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
        answer_text = f'{ emojies.sparkles } { player.nickname }, Такой команды нет. Возможно, вы имели в виду:\n\n'
        for i in range(len(matches)):
            answer_text += f'{ emojies.numbers[i+1] } { matches[i] }\n'
        answer_text += f'\n\nВведите "помощь", чтобы получить список доступных команд'
        await m.answer(answer_text)
    else:
        answer_text = f'{ emojies.sparkles } { player.nickname }, Такой команды нет\nВведите "помощь", чтобы получить список доступных команд.'
        await m.answer(answer_text)