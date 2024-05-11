# imports
# vkbottle
from vkbottle.bot import Message
# database
from database.repository import Repository
from database.entities import EnergyEntity
# utils
from utils.ts_now import ts_now
# local folder
from .get_energy import get_energy

# repos
energyRepo = Repository(entity=EnergyEntity())

# funcs
async def use_energy(user_id: int, amount: int = 1):
    # entities
    energy: EnergyEntity = await energyRepo.find_one_by({ 'user_id': user_id })
    # calculate player energy ( current + accumulated )
    player_energy = await get_energy(user_id) # return round(current + accumulated)
    if player_energy > energy.energy_limit:
        player_energy = energy.energy_limit
    # ... 
    await energyRepo.update({ 'user_id': user_id }, { 'energy': player_energy - amount }) # update currrent energy
    await energyRepo.update({ 'user_id': user_id }, { 'ts_previous_use': ts_now() }) # update ts_previous_use