# imports
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
from keyboards import keyboards
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity
from rules import PayloadContainsOrTextRule

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'back_to_start' }, text='начать'))
async def start(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id }) # get user from db
    # answer
    text = f'{ emojies.sparkles } { player.nickname }, Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards['start']
    await m.answer(message=text, keyboard=keyboard)


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_general' }))
async def show_general(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ emojies.alien_monster } { player.nickname }, Основное:'
    keyboard = keyboards['general']
    await m.answer(message=text, keyboard=keyboard)