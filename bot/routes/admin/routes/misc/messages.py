from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, EnergyEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
# acs
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())

# handlers

# ---------------------------------------- MESSAGE SEND ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/message <pid> <text>',
        '/message <pid>',
        '/message',
        '/m <pid> <text>',
        '/m <pid>',
        '/m',
    ]
)
async def message_send(m: Message, pid=None, text=None):
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
    
    # send message
    text_builded = f'''{ emojies.mail } { recipient.nickname }, Сообщение от @id{player.user_id}(администратора):

    {text}
    '''.replace('    ', '')
    await m.ctx_api.messages.send(
        user_id=recipient.user_id,
        peer_id=recipient.user_id,
        random_id=0,
        message=text_builded
    )

    # acs answer
    acs_response = 'Сообщение отправлено'
    await acs_success(m, acs_response)