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
# tools
from tools.ts2date import ts2date

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_profile' }, text='профиль'))
async def profile(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    registration_date = ts2date(player.ts_registration)

    text = f'''{ emojies.ledger } { player.nickname }, Ваш профиль:

    { emojies.symbol_id } Игровой ID: { player.player_id }
    { emojies.scroll } Никнейм: { player.nickname }
    { emojies.dollar_banknote } Деньги: { player.money:,}$
    { emojies.trophy } Опыт: { player.experience }
    { emojies.coin } Донат валюта: { player.special_currency }
    { emojies.watch } Дата регистрации: { registration_date }
    '''.replace('    ', '')

    await m.answer(text)