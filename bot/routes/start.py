# imports
from vkbottle.bot import BotLabeler, Message
from keyboards import keyboards
from emojies import emojies
from database.repository import Repository
from database.entities import MainEntity

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

mainRepo = Repository(entity=MainEntity())

# handlers
@bl.message(text='начать')
async def start(m: Message):
    # get user from db
    user: MainEntity = mainRepo.find_one_by({'user_id': 230990098})
    # answer
    text = f'{ emojies.sparkles } { user.nickname }, Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards['start']
    await m.answer(message=text, keyboard=keyboard)


@bl.message(text='change')
async def change(m: Message):
    try:
        mainRepo.update(where={ 'user_id': 230990098 }, field={ 'nickname': 'haha' })
        await m.answer(f'success')
    except:
        await m.answer(f'err')