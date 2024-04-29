# imports
# vkbottle
from vkbottle.bot import Message
# utils
from utils.ts_now import ts_now
# database
from database.repository import Repository
from database.entities import PlayerEntity, EnergyEntity
# constants
from constants import max_player_energy as MAX_PLAYER_ENERGY
from constants import energy_recovery_time_in_minutes as ENERGY_RECOVERY_TIME_IN_MINUTES

# repos
energyRepo = Repository(entity=EnergyEntity())

# funcs
async def get_energy(user_id: int):
    # entities
    energy: EnergyEntity = await energyRepo.find_one_by({ 'user_id': user_id })
    ts_previous_use = energy.ts_previous_use # ...
    # ts as mins
    ts_now_as_mins = round(ts_now() / 60)
    ts_previous_use_as_mins = round(ts_previous_use / 60)
    # ccalculate energy
    accumulated_energy = (ts_now_as_mins - ts_previous_use_as_mins) / ENERGY_RECOVERY_TIME_IN_MINUTES
    current_energy = energy.energy
    return round(current_energy + accumulated_energy)