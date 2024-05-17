from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
# consts
from constants import game_roles
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers

# ---------------------------------------- MONEY GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/money get <pid>',
        '/money get',
        '/mo g <pid>',
        '/mo g',
    ]
)
async def money_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'money_get')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Деньги @id{recipient.user_id}(игрока): ${recipient.money:,} { emojies.dollar_banknote }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- MONEY ADD ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/money add <pid> <amount>',
        '/money add <pid>',
        '/money add',
        '/mo a <pid> <amount>',
        '/mo a <pid>',
        '/mo a',
    ]
)
async def money_add(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'money_add')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'money_add')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates
    # set nickname
    playerRepo.update({ 'player_id': int(pid) }, { 'money': recipient.money + int(amount) })
    
    # acs answer
    acs_response = f'-- + ${int(amount):,} { emojies.dollar_banknote } для @id{recipient.user_id}(игрока)'
    await acs_success(m, acs_response)








# ---------------------------------------- MONEY REDUCE ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/money reduce <pid> <amount>',
        '/money reduce <pid>',
        '/money reduce',
        '/mo r <pid> <amount>',
        '/mo r <pid>',
        '/mo r',
    ]
)
async def money_reduce(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'money_reduce')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'money_reduce')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates
    # money reduce
    
    # check if result of calculate < zero
    result = recipient.money - int(amount)
    playerRepo.update({ 'player_id': int(pid) }, { 'money': 0 if result < 0 else result })
    
    # acs answer
    acs_response = f'-- - ${int(amount):,} { emojies.dollar_banknote } для @id{recipient.user_id}(игрока)'
    await acs_success(m, acs_response)