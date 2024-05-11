from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, EnergyEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
from utils.ts2date import ts2date
# tools
from tools.get_player_profile_text import get_player_profile_text
# consts
from constants import game_roles
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())

# handlers

# ---------------------------------------- PROFILE GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/profile get <pid>',
        '/profile get',
        '/pr g <pid>',
        '/pr g',
    ]
)
async def profile_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'profile_get')
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        await acs_player_not_found(m)
        return
    # acs answer
    profile_linestext = await get_player_profile_text(recipient.player_id)

    acs_response = f'''Полученные данные:
    -- Профиль @id{recipient.user_id}(игрока):

    {profile_linestext}
    '''.replace('    ', '')
    await acs_success(m, acs_response)