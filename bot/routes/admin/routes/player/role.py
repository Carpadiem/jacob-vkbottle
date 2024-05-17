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

# ---------------------------------------- ROLE GET ----------------------------------------

# middleware checks:
# 
# GET:
# try validation
# try get recipient
# 
# SET:
# try validation
# 
# 
# 
# 
# 
# 
# 

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/role get <pid>',
        '/role get',
        '/ro g <pid>',
        '/ro g',
    ]
)
async def role_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'role_get')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    
    # acs answer
    acs_response = f'''Полученные данные:
    -- Роль @id{recipient.user_id}(игрока): { recipient.role.capitalize() }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- ROLE SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/role set <pid> <role>',
        '/role set <pid>',
        '/role set',
        '/ro s <pid> <role>',
        '/ro s <pid>',
        '/ro s',
    ]
)
async def role_set(m: Message, pid=None, role=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'role_set')
        return
    if role == None:
        await acs_usage_error(m, 'role_set')
        return
    # check if role exist in game
    role = role.lower()
    if role not in game_roles:
        await acs_error(m, 'Такой роли нет. Список ролей для выдачи можно посмотреть на сайте https://jacobgame.ru')
        return
    # u cant give role to yourself
    if int(pid) == player.player_id:
        await acs_error(m, 'Вы не можете выдать роль самому себе')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates
    # set role
    playerRepo.update({ 'player_id': int(pid) }, { 'role': role })
    
    # acs answer
    acs_response = f'-- Новая роль для @id{recipient.user_id}(игрока): { str(role).capitalize() }'
    await acs_success(m, acs_response)