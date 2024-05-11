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

# ---------------------------------------- BANK SCORE GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score get <pid>',
        '/bank score get',
        '/bs g <pid>',
        '/bs g',
    ]
)
async def bank_score_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_score_get')
        return
    # get recipient bank
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Счет банка @id{recipient_bank.user_id}(игрока): ${recipient_bank.score:,} { emojies.dollar_banknote }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- BANK SCORE ADD ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score add <pid> <role>',
        '/bank score add <pid>',
        '/bank score add',
        '/bs a <pid> <role>',
        '/bs a <pid>',
        '/bs a',
    ]
)
@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank add <pid> <amount>',
        '/bank add <pid>',
        '/bank add',
        '/ba a <pid> <amount>',
        '/ba a <pid>',
        '/ba a',
    ]
)
async def bank_score_add(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_score_add')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'bank_score_add')
        return
    # get recipient
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # updates
    # add bank score
    await bankRepo.update({ 'player_id': int(pid) }, { 'score': recipient_bank.score + int(amount) })
    
    # acs answer
    acs_response = f'-- + ${int(amount):,} { emojies.dollar_banknote } на счет банка для @id{recipient_bank.user_id}(игрока)'
    await acs_success(m, acs_response)








# ---------------------------------------- BANK SCORE REDUCE ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score add <pid> <role>',
        '/bank score add <pid>',
        '/bank score add',
        '/bs a <pid> <role>',
        '/bs a <pid>',
        '/bs a',
    ]
)
@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score reduce <pid> <amount>',
        '/bank score reduce <pid>',
        '/bank score reduce',
        '/bs r <pid> <amount>',
        '/bs r <pid>',
        '/bs r',
    ]
)
async def bank_score_reduce(m: Message, pid=None, amount=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_score_reduce')
        return
    if not is_number(amount):
        await acs_usage_error(m, 'bank_score_reduce')
        return
    # get recipient
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # updates
    # add bank score
    result = recipient_bank.score - int(amount)
    await bankRepo.update({ 'player_id': int(pid) }, { 'score': 0 if result < 0 else result })
    # acs answer
    acs_response = f'-- - ${int(amount):,} { emojies.dollar_banknote } со счета банка для @id{recipient_bank.user_id}(игрока)'
    await acs_success(m, acs_response)