# imports
from random import randint
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import PhotoMessageUploader
from vkbottle.dispatch.rules.base import PayloadContainsRule
from keyboards import keyboards
from emojies import emojies
# database
from database.repository import Repository
from database.entities import PlayerEntity
# tools
from tools import error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'report' }))
async def report(m: Message):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.mount } { player.nickname }, Напишите "репорт [текст]", чтобы отправить ваше сообщение в поддержку'
    await m.answer(text)


@bl.message(text=['репорт <text>', 'репорт'])
async def report_text(m: Message, text=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    # validation
    if text == None:
        text = f'{ emojies.sparkles } { player.nickname }, Введите текст репорта. Пример: "репорт [текст]"'
        await error_message(m, text)
        return
    
    # success
    player_text = f'''{ emojies.red_triangle } { player.nickname }, Спасибо за обращение! Если потребуется, поддержка свяжется с вами в течении 30 минут.

    { emojies.like } Желаем приятных игр :)
    '''.replace('    ', '')
    await m.answer(player_text)

    # manager answer
    manager_text = f'''{ emojies.red_envelope } @id{m.from_id}(Пользователь) отправил репорт:

    "{text}"
    '''.replace('    ', '')
    await m.ctx_api.messages.send(
        user_id=230990098,
        peer_id=230990098,
        random_id=0,
        message=manager_text,
    )