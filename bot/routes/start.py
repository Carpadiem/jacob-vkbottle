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
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id }) # get user from db
    # answer
    text = f'{ emojies.sparkles } { player.nickname }, Добро пожаловать в игру! Введите "помощь", чтобы получить список доступных команд.'
    keyboard = keyboards['start']
    await m.answer(message=text, keyboard=keyboard)


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_general' }))
async def show_general(m: Message):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ emojies.alien_monster } { player.nickname }, Основное:'
    await m.answer(message=text, keyboard=keyboards['general'])


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_games' }))
async def show_games(m: Message):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ emojies.cube } { player.nickname }, Игры:'
    await m.answer(message=text, keyboard=keyboards['games'])


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_misc' }))
async def show_misc(m: Message):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ emojies.alien_monster } { player.nickname }, Разное:'
    await m.answer(message=text, keyboard=keyboards['misc'])