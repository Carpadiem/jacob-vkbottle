from vkbottle.bot import BotLabeler, Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity, CasesEntity
from rules import RoleRule
# utils
from utils.is_number import is_number
# acs
from routes.admin.acs.output import acs_usage_error, acs_success, acs_error, acs_player_not_found
# consts
from constants import game_cases


# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# init repo
playerRepo = Repository(entity=PlayerEntity())
casesRepo = Repository(entity=CasesEntity())

# handlers

# ---------------------------------------- CASES GET ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/cases get <pid>',
        '/cases get',
        '/ca g <pid>',
        '/ca g',
    ]
)
async def cases_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        await acs_usage_error(m, 'cases_get')
        return
    # get recipient bank
    recipient_cases: CasesEntity = casesRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_cases == None:
        await acs_player_not_found(m)
        return
    
    # acs answer
    recipient_user_id = recipient_cases.user_id
    cases_text = ''
    player_cases_as_dict = recipient_cases.__dict__
    del player_cases_as_dict['table_name']
    del player_cases_as_dict['player_id']
    del player_cases_as_dict['user_id']

    for column_name, case_count in player_cases_as_dict.items():
        case_id = int(column_name.split('_')[1])
        case_name: str = game_cases[case_id]['name']
        case_name = case_name.capitalize()
        cases_text += f'{ emojies.option } { case_name }: {case_count:,} шт.\n'

    acs_response = f'''Полученные данные:
    -- Кейсы @id{ recipient_user_id }(игрока):

    {cases_text}
    '''.replace('    ', '')
    await acs_success(m, acs_response)








# ---------------------------------------- CASES ADD ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/cases add <pid> <cid> <amount>',
        '/cases add <pid> <cid>',
        '/cases add <pid>',
        '/cases add',
        '/ca a <pid> <cid> <amount>',
        '/ca a <pid> <cid>',
        '/ca a <pid>',
        '/ca a',
    ]
)
async def cases_add(m: Message, pid=None, cid=None, amount=None):
    # entites
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid): await acs_usage_error(m, 'cases_add'); return
    if not is_number(cid): await acs_usage_error(m, 'cases_add'); return
    if not is_number(amount): await acs_usage_error(m, 'cases_add'); return
    
    game_cases_count = 0
    for k, v in game_cases.items():
        game_cases_count += 1

    if int(cid) < 0 or int(cid) > game_cases_count:
        await acs_usage_error(m, 'cases_add')
        return

    # get recipient
    recipient_cases: CasesEntity = casesRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_cases == None:
        await acs_player_not_found(m)
        return
    
    # check value > recipient_bank.transfers_limit OR value < 0
    if int(amount) < 0:
        await acs_error(m, 'Значение должно быть больше 0')
        return

    # updates
    # cases add
    recipient_case_by_cid = recipient_cases.__dict__[f'count_{cid}']
    casesRepo.update({ 'player_id': int(pid) }, { f'count_{cid}': recipient_case_by_cid + int(amount) }) 
    # acs answer
    case_name = game_cases[int(cid)]['name']
    acs_response = f'-- + {amount} кейсов "{case_name}" для @id{recipient_cases.user_id}(игрока)'
    await acs_success(m, acs_response)








# ---------------------------------------- CASES REDUCE ----------------------------------------

@bl.message(
    RoleRule(['founder', 'owner', 'administrator']),
    text=[
        '/cases reduce <pid> <cid> <amount>',
        '/cases reduce <pid> <cid>',
        '/cases reduce <pid>',
        '/cases reduce',
        '/ca r <pid> <cid> <amount>',
        '/ca r <pid> <cid>',
        '/ca r <pid>',
        '/ca r',
    ]
)
async def cases_reduce(m: Message, pid=None, cid=None, amount=None):
    # entites
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid): await acs_usage_error(m, 'cases_reduce'); return
    if not is_number(cid): await acs_usage_error(m, 'cases_reduce'); return
    if not is_number(amount): await acs_usage_error(m, 'cases_reduce'); return
    
    game_cases_count = 0
    for k, v in game_cases.items():
        game_cases_count += 1

    if int(cid) < 0 or int(cid) > game_cases_count:
        await acs_usage_error(m, 'cases_reduce')
        return

    # get recipient
    recipient_cases: CasesEntity = casesRepo.find_one_by({ 'player_id': int(pid) })
    if recipient_cases == None:
        await acs_player_not_found(m)
        return
    
    if int(amount) < 0 or int(amount) > 100:
        await acs_error(m, 'Значение должно быть в пределах 0-100')
        return

    # updates
    # cases reduce
    recipient_case_by_cid = recipient_cases.__dict__[f'count_{cid}']
    update_result = recipient_case_by_cid - int(amount)
    casesRepo.update({ 'player_id': int(pid) }, { f'count_{cid}': 0 if update_result < 0 else update_result }) 
    # acs answer
    case_name = game_cases[int(cid)]['name']
    acs_response = f'-- - {amount} кейсов "{case_name}" для @id{recipient_cases.user_id}(игрока)'
    await acs_success(m, acs_response)