# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity
from database.repository import Repository
# emojies
from emojies import emojies
# keyboards
from keyboards import keyboards

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(
    payload={ 'action_type': 'button', 'action': 'motor_transport' },
    text=[
        'транспорт',
    ]
))
async def vehicle(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.car } { player.nickname }, Добро пожаловать в меню автотранспорта

    { emojies.tip } Выберите из меню, куда хотите попасть
    '''.replace('    ', '')
    await m.answer(message=text, keyboard=keyboards['motor_transport_start'])