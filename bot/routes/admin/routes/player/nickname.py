# imports
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
from keyboards import keyboards
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity
from rules import RoleRule
# tools
from tools import error_message
# utils
from utils.is_number import is_number
# consts
from constants import game_roles
# acs output
from routes.admin.acs.output import acs_usage_error, acs_player_not_found, acs_error, acs_success

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers

# ---------------------------------------- NICKNAME GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/nickname get <pid>',
        '/nickname get',
        '/ni g <pid>',
        '/ni g',
    ],
) 
async def nickname_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'nickname_get')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    
    # acs answer
    acs_response = f'''Полученные данные:
    -- Никнейм @id{recipient.user_id}(игрока): { recipient.nickname }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- NICKNAME SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/nickname set <pid> <text>',
        '/nickname set <pid>',
        '/nickname set',
        '/ni s <pid> <text>',
        '/ni s <pid>',
        '/ni s',
    ],
)
async def nickname_set(m: Message, pid=None, text=None):
    # entites
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'nickname_set')
        return
    if text == None:
        await acs_usage_error(m, 'nickname_set')
        return
    # get recipient
    recipient: PlayerEntity = playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # updates
    # set nickname
    playerRepo.update({ 'player_id': int(pid) }, { 'nickname': text })
    
    # acs answer
    acs_response = f'-- Новый никнейм для @id{recipient.user_id}(игрока): { text }'
    await acs_success(m, acs_response)