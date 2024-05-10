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

# ---------------------------------------- BANK TRANSFERS GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank transfers get <pid>',
        '/bank transfers get',
        '/bt g <pid>',
        '/bt g',
    ]
)
async def bank_transfers_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_transfers_get')
        return
    # get recipient bank
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Текущее количество переводов в банке у @id{recipient_bank.user_id}(игрока): { recipient_bank.transfers }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- BANK TRANSFERS SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank transfers set <pid> <value>',
        '/bank transfers set <pid>',
        '/bank transfers set',
        '/bt s <pid> <value>',
        '/bt s <pid>',
        '/bt s',
    ]
)
async def bank_transfers_set(m: Message, pid=None, value=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_transfers_set')
        return
    if not is_number(value):
        await acs_usage_error(m, 'bank_transfers_set')
        return
    # get recipient
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return

    # check value > recipient_bank.transfers_limit OR value < 0
    if int(value) > recipient_bank.transfers_limit or int(value) < 0:
        text = f'''Лимит переводов у этого @id{recipient_bank.user_id}(игрока): { recipient_bank.transfers_limit } шт.

        Вы не можете установить значение больше лимита или меньше 0
        '''.replace('    ', '')
        await acs_error(m, text)
        return

    # updates
    await bankRepo.update({ 'player_id': int(pid) }, { 'transfers': int(value) })
    
    # acs answer
    acs_response = f'-- Новое количество переводов для @id{recipient_bank.user_id}(игрока): { int(value) }'
    await acs_success(m, acs_response)