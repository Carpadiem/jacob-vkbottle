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

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_money' }, text='деньги'))
async def money(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    text = f'{ player.nickname }, У вас ${player.money:,} {emojies.dollar_banknote}'
    await m.answer(text)