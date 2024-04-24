# imports
from vkbottle.bot import BotLabeler, Message
from keyboards import keyboards

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# handlers
@bl.message(text='начать')
async def welcome(m: Message):    
    text = f'Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards.get('start')
    await m.answer(message=text, keyboard=keyboard)
