# imports
from vkbottle.bot import Message
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity


# init repo
playerRepo = Repository(entity=PlayerEntity())


# acs usage example texts
usage_example_acs = {
    'role_get': '/role get [игровой ID: int]',
    'role_set': '/role set [игровой ID: int] [роль: str]',

    'nickname_get': '/nickname get [игровой ID: int]',
    'nickname_set': '/nickname set [игровой ID: int] [текст: str]',

    'money_get': '/money get [игровой ID: int]',
    'money_add': '/money add [игровой ID: int] [количество: int]',
    'money_reduce': '/money reduce [игровой ID: int] [количество: int]',
}


async def acs_usage_error(m: Message, example_identificator: str):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    acs_output_text = f'[𝙰𝙲𝚂]: { emojies.scroll } { player.nickname }, Пример использования команды:\n\n{ usage_example_acs[example_identificator] }'
    await m.answer(acs_output_text)

async def acs_player_not_found(m: Message):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    acs_output_text = f'[𝙰𝙲𝚂]: { emojies.crossmark } { player.nickname }, Игрока с таким ID нет'
    await m.answer(acs_output_text)

async def acs_error(m: Message, error_text: str):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    acs_output_text = f'[𝙰𝙲𝚂]: { emojies.crossmark } { player.nickname }, { error_text }'
    await m.answer(acs_output_text)

async def acs_success(m: Message, acs_response: str):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    acs_output_text = f'''[𝙰𝙲𝚂]: { emojies.checkmark } { player.nickname }, Успешное выполнение операции
    
    { emojies.abc_button } Ответ системы ACS:

    { acs_response }
    '''.replace('    ', '')
    await m.answer(acs_output_text)