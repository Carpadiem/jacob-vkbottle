# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity, EnergyEntity
from database.repository import Repository
# emojies
from emojies import emojies
# utils
from utils.ts2date import ts2date
from tools import get_energy
# constants
from constants import max_player_energy as MAX_PLAYER_ENERGY

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())


# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_profile' }, text='профиль'))
async def profile(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # ...
    registration_date = ts2date(player.ts_registration)
    player_energy = await get_energy(m.from_id)

    if player_energy > MAX_PLAYER_ENERGY:
        player_energy = MAX_PLAYER_ENERGY

    text = f'''{ emojies.ledger } { player.nickname }, Ваш профиль:

    { emojies.symbol_id } Игровой ID: { player.player_id }
    { emojies.scroll } Никнейм: { player.nickname }
    { emojies.dollar_banknote } Деньги: {player.money:,}$
    { emojies.high_voltage } Энергия: {player_energy:,}
    { emojies.trophy } Опыт: { player.experience }
    { emojies.coin } Донат валюта: { player.special_currency }
    { emojies.watch } Дата регистрации: { registration_date }
    '''.replace('    ', '')

    await m.answer(text)