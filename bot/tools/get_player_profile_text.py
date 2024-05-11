from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, EnergyEntity
from utils.ts2date import ts2date
from tools.get_energy import get_energy

# init repo
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())


async def get_player_profile_text(player_id: int):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'player_id': player_id })
    energy: EnergyEntity = await energyRepo.find_one_by({ 'player_id': player.player_id })
    
    # energy calculation
    player_energy = await get_energy(player.user_id)
    if player_energy > energy.energy_limit:
        player_energy = energy.energy_limit
    
    # acs answer
    linestext_profile = f'''
    { emojies.symbol_id } Игровой ID: { player.player_id }
    { emojies.scroll } Никнейм: { player.nickname }
    { emojies.dollar_banknote } Деньги: ${player.money:,}
    { emojies.high_voltage } Энергия: { player_energy }/{ energy.energy_limit }
    { emojies.trophy } Опыт: {player.experience:,}
    { emojies.coin } Донат валюта: {player.special_currency:,}
    { emojies.watch } Дата регистрации: { ts2date(player.ts_registration) }
    '''.replace('    ', '')

    return linestext_profile