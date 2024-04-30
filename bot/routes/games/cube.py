# imports
from random import randint, randrange
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity
from database.repository import Repository
# emojies
from emojies import emojies
# keyboard
from keyboards import keyboards
# tools
from tools import error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'game_cube' }, text=['кубик', 'куб']))
async def cube(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ player.nickname }, Выберите число [1-6]:'
    await m.answer(message=text, keyboard=keyboards['game_cube'])


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'play_cube' }))
async def play_cube(m: Message):
    # get payload from message
    payload = m.get_payload_json()
    cube_number = payload['cube_number']
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # win or lose?
    random_number = randint(1, 6)
    if cube_number != random_number:
        text = f'{ emojies.cube } { player.nickname }, На кубике выпало число {random_number}. Попробуйте еще раз'
        await error_message(m, text)
        return
    # db updates
    reward_money = randrange(5, 25, 5) * 100 # describe the reward
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + reward_money }) # update player's money
    # answer
    text = f'''{ emojies.cube }{ emojies.comet } { player.nickname } Вы угадали

    { emojies.bomb } Награда: ${reward_money} { emojies.dollar_banknote }
    '''.replace('    ', '')
    await m.answer(text)

