from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, BankEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
# consts
from constants import game_roles
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found

# middlewares
from middlewares import acs_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True
bl.message_view.register_middleware(acs_message)

# init repo
playerRepo = Repository(entity=PlayerEntity())
bankRepo = Repository(entity=BankEntity())

# handlers

# ---------------------------------------- BANK TRANSFERS LIMIT GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank transfers limit get <pid>',
        '/bank transfers limit get',
        '/btl g <pid>',
        '/btl g',
    ]
)
async def bank_transfers_limit_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_transfers_limit_get')
        return
    # get recipient bank
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Лимит переводов в банке у @id{recipient_bank.user_id}(игрока): { recipient_bank.transfers_limit }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- BANK TRANSFERS SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank transfers limit set <pid> <value>',
        '/bank transfers limit set <pid>',
        '/bank transfers limit set',
        '/btl s <pid> <value>',
        '/btl s <pid>',
        '/btl s',
    ]
)
async def bank_transfers_limit_set(m: Message, pid=None, value=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_transfers_limit_set')
        return
    if not is_number(value):
        await acs_usage_error(m, 'bank_transfers_limit_set')
        return
    # get recipient
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return

    # check value > recipient_bank.transfers_limit OR value < 0
    if int(value) < 0:
        await acs_error(m, 'Вы не можете установить значение меньше 0')
        return

    # updates
    await bankRepo.update({ 'player_id': int(pid) }, { 'transfers_limit': int(value) })
    
    # acs answer
    acs_response = f'-- Новый лимит переводов для @id{recipient_bank.user_id}(игрока): { int(value) }'
    await acs_success(m, acs_response)