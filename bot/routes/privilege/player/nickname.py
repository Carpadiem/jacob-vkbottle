# imports
from typing import Tuple
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
# rules
from rules import PayloadContainsOrTextRule
# database
from database.repository import Repository
from database.entities import PlayerEntity, PropertyEntity
# emojies
from emojies import emojies
# utils
from utils.is_number import is_number
# tools
from tools import error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
propertyRepo = Repository(entity=PropertyEntity())

# PCS - privileged command system

# handers
@bl.message(text=[
    '/nickname set <pid> <text>',
    '/nickname set <pid>',
    '/nickname set',
    '/ni s <pid> <text>',
    '/ni s <pid>',
    '/ni s',
])
async def nickname_set(m: Message, pid=None, text=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /nickname set [игровой айди] [текст]'
        await error_message(m, error_text)
        return
    if text == None:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /nickname set [игровой айди] [текст]'
        await error_message(m, error_text)
        return
    # update nickname
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': int(pid) })
    if recipient == None:
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Игрока с таким ID нет'
        await error_message(m, error_text)
        return
    await playerRepo.update({ 'player_id': recipient.player_id }, { 'nickname': text })
    # answer
    answer_text = f'''[𝙿𝙲𝚂]: { emojies.checkmark } Успешное выполнение операции

    -- Новый никнейм для @id{recipient.user_id}(игрока): { text }
    '''.replace('    ', '')
    await m.answer(answer_text)




@bl.message(text=[
    '/nickname get <pid>',
    '/nickname get',
    '/ni g <pid>',
    '/ni g',
])
async def nickname_get(m: Message, pid=None):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if not is_number(pid):
        error_text = f'[𝙿𝙲𝚂]: { emojies.crossmark } { player.nickname }, Пример использования команды: /nickname set [игровой айди] [текст]'
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
    -- Никнейм @id{recipient.user_id}(игрока): { recipient.nickname }
    '''.replace('    ', '')
    await m.answer(answer_text)