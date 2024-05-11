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

# ---------------------------------------- ENERGY GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/energy get <pid>',
        '/energy get',
        '/en g <pid>',
        '/en g',
    ]
)
async def energy_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'energy_get')
        return
    # get recipient bank
    recipient_energy: EnergyEntity = await energyRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_energy == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Энергия @id{recipient_energy.user_id}(игрока): { recipient_energy.energy }/{ recipient_energy.energy_limit } { emojies.high_voltage }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- ENERGY SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/energy set <pid> <value>',
        '/energy set <pid>',
        '/energy set',
        '/en s <pid> <value>',
        '/en s <pid>',
        '/en s',
    ]
)
async def energy_set(m: Message, pid=None, value=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'energy_set')
        return
    if not is_number(value):
        await acs_usage_error(m, 'energy_set')
        return
    # get recipient
    recipient_energy: EnergyEntity = await energyRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_energy == None:
        await acs_player_not_found(m)
        return
    
    # check value > recipient_bank.transfers_limit OR value < 0
    if int(value) > recipient_energy.energy_limit or int(value) < 0:
        text = f'''Лимит энергии у этого @id{recipient_energy.user_id}(игрока): { recipient_energy.energy_limit }

        Вы не можете установить значение больше лимита или меньше 0
        '''.replace('    ', '')
        await acs_error(m, text)
        return

    # updates
    # energy set
    await energyRepo.update({ 'player_id': int(pid) }, { 'energy': int(value) })
    await energyRepo.update({ 'player_id': int(pid) }, { 'ts_previous_use': ts_now() })
    
    # acs answer
    acs_response = f'-- Новое значение энергии для @id{recipient_energy.user_id}(игрока): { int(value) }/{ recipient_energy.energy_limit } { emojies.high_voltage }'
    await acs_success(m, acs_response)