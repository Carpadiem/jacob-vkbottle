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

# ---------------------------------------- BANK SCORE LIMIT GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score limit get <pid>',
        '/bank score limit get',
        '/bsl g <pid>',
        '/bsl g',
    ]
)
async def bank_score_limit_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_score_limit_get')
        return
    # get recipient bank
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    # acs answer
    acs_response = f'''Полученные данные:
    -- Лимит банковского счета @id{recipient_bank.user_id}(игрока): ${recipient_bank.score_limit:,} { emojies.dollar_banknote }
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- BANK SCORE LIMIT SET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank score limit set <pid> <value>',
        '/bank score limit set <pid>',
        '/bank score limit set',
        '/bsl s <pid> <value>',
        '/bsl s <pid>',
        '/bsl s',
    ]
)
async def bank_score_limit_set(m: Message, pid=None, value=None):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'bank_score_limit_set')
        return
    if not is_number(value):
        await acs_usage_error(m, 'bank_score_limit_set')
        return
    # get recipient
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_bank == None:
        await acs_player_not_found(m)
        return
    
    # check if value > zero
    if int(value) < 0:
        await acs_error(m, 'Значение должно быть больше 0')
        return

    # updates
    # set bank score limit
    await bankRepo.update({ 'player_id': int(pid) }, { 'score_limit': int(value) })
    
    # acs answer
    acs_response = f'-- Новый лимит счета банка для @id{recipient_bank.user_id}(игрока): ${int(value):,}'
    await acs_success(m, acs_response)








# ---------------------------------------- BANK SCORE ADD ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank add <pid> <role>',
        '/bank add <pid>',
        '/bank add',
        '/ba a <pid> <role>',
        '/ba a <pid>',
        '/ba a',
    ]
)
@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/bank reduce <pid> <amount>',
        '/bank reduce <pid>',
        '/bank reduce',
        '/ba r <pid> <amount>',
        '/ba r <pid>',
        '/ba r',
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