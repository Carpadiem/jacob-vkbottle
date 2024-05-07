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

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers
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
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /role set [игровой айди] [роль]'
        await error_message(m, error_text)
        return
    if role == None:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /ro s [игровой айди] [роль]'
        await error_message(m, error_text)
        return
    # check if role exist in game
    if role not in game_roles:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Такой роли нет. Список ролей для выдачи можно посмотреть на сайте https://jacobgame.ru'
        await error_message(m, error_text)
        return
    # u cant give role to yourself
    if int(pid) == player.player_id:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Вы не можете выдать роль самому себе'
        await error_message(m, error_text)
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Игрока с таким ID нет'
        await error_message(m, error_text)
        return
    # updates
    # set role
    await playerRepo.update({ 'player_id': int(pid) }, { 'role': role })
    # answer
    answer_text = f'''[𝙿𝙲𝚂]: { emojies.checkmark } Успешное выполнение операции

    -- Роль @id{recipient.user_id}(игрока): { str(role).capitalize() }
    '''.replace('    ', '')
    await m.answer(answer_text)




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
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /role set [игровой айди] [роль]'
        await error_message(m, error_text)
        return
    # get recipient
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Игрока с таким ID нет'
        await error_message(m, error_text)
        return
    # answer
    answer_text = f'''[𝙿𝙲𝚂]: { emojies.checkmark } Успешное выполнение операции

    { emojies.abc_button } Полученные данные:
    -- Роль @id{recipient.user_id}(игрока): { recipient.role.capitalize() }
    '''.replace('    ', '')
    await m.answer(answer_text)