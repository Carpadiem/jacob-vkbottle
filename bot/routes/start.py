# imports
from vkbottle.bot import BotLabeler, Message
from keyboards import keyboards
from emojies import emojies

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# handlers
@bl.message(text='начать')
async def start(m: Message):
    text = f'{ emojies.sparkles } Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards['start']
    await m.answer(message=text, keyboard=keyboard)