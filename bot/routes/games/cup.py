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
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'game_cup' }, text=['стакан', 'стаканчик']))
async def cup(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ player.nickname }, Выберите число [1-3]:'
    await m.answer(message=text, keyboard=keyboards['game_cup'])


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'play_cup' }))
async def play_cup(m: Message):
    # get payload from message
    payload = m.get_payload_json()
    cup_number = payload['cup_number']
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # win or lose?
    random_number = randint(1, 3)
    if cup_number != random_number:
        text = f'{ emojies.cup } { player.nickname }, Это был {random_number} стакан. Попробуйте еще раз'
        await error_message(m, text)
        return
    # db updates
    reward_money = randrange(5, 15, 5) * 100 # describe the reward
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + reward_money }) # update player's money
    # answer
    text = f'''{ emojies.cup }{ emojies.alien_monster } { player.nickname } Вы угадали

    { emojies.red_envelope } Награда: ${reward_money} { emojies.dollar_banknote }
    '''.replace('    ', '')
    await m.answer(text)

