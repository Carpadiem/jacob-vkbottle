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

# ---------------------------------------- EXPERIENCE GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/exp get <pid>',
        '/exp get',
        '/ex g <pid>',
        '/ex g',
    ]
)
async def exp_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'exp_get')
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Опыт @id{recipient.user_id}(игрока): {recipient.experience:,} { emojies.trophy }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- EXPERIENCE ADD ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/exp add <pid> <amount>',
        '/exp add <pid>',
        '/exp add',
        '/ex a <pid> <amount>',
        '/ex a <pid>',
        '/ex a',
    ]
)
async def exp_add(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'exp_add')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'exp_add')
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates
    # set nickname
    await playerRepo.update({ 'player_id': int(pid) }, { 'experience': recipient.experience + int(amount) })
    
    # acs answer
    acs_response = f'-- + {int(amount):,} { emojies.trophy } для @id{recipient.user_id}(игрока)'
    await acs_success(m, acs_response)








# ---------------------------------------- EXPERIENCE REDUCE ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/exp reduce <pid> <amount>',
        '/exp reduce <pid>',
        '/exp reduce',
        '/ex r <pid> <amount>',
        '/ex r <pid>',
        '/ex r',
    ]
)
async def exp_reduce(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'exp_reduce')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'exp_reduce')
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates

    # exp reduce
    result = recipient.experience - int(amount)
    await playerRepo.update({ 'player_id': int(pid) }, { 'experience': 0 if result < 0 else result })
    # acs answer
    acs_response = f'-- - {int(amount):,} { emojies.trophy } для @id{recipient.user_id}(игрока)'
    await acs_success(m, acs_response)