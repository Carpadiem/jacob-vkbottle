from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, EnergyEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
from utils.ts_now import ts_now
# acs
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found
# middlewares
from middlewares import acs_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True
bl.message_view.register_middleware(acs_message)

# init repo
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())

# handlers

# ---------------------------------------- ENERGY LIMIT GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/energy limit get <pid>',
        '/energy limit get',
        '/enl g <pid>',
        '/enl g',
    ]
)
async def energy_limit_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'energy_limit_get')
        return
    # get recipient bank
    recipient_energy: EnergyEntity = await energyRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_energy == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Лимит энергии @id{recipient_energy.user_id}(игрока): { recipient_energy.energy_limit }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- ENERGY SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/energy limit set <pid> <value>',
        '/energy limit set <pid>',
        '/energy limit set',
        '/enl s <pid> <value>',
        '/enl s <pid>',
        '/enl s',
    ]
)
async def energy_limit_set(m: Message, pid=None, value=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'energy_limit_set')
        return
    if not is_number(value):
        await acs_usage_error(m, 'energy_limit_set')
        return
    # get recipient
    recipient_energy: EnergyEntity = await energyRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_energy == None:
        await acs_player_not_found(m)
        return
    
    # check if value > zero
    if int(value) < 0 or int(value) > 500:
        await acs_error(m, 'Значение должно быть в пределах 0-500')
        return

    # updates
    # energy set
    await energyRepo.update({ 'player_id': int(pid) }, { 'energy_limit': int(value) })
    
    # acs answer
    acs_response = f'-- Новое значение лимита энергии для @id{recipient_energy.user_id}(игрока): { int(value) }'
    await acs_success(m, acs_response)