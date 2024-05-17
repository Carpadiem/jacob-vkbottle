# imports
from random import randint
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import PhotoMessageUploader
from vkbottle.dispatch.rules.base import PayloadContainsRule
from keyboards import keyboards
from emojies import emojies
from database.repository import Repository
from database.entities import PlayerEntity

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# init repo
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'picture' }))
async def picture(m: Message):
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })

    # uploader
    uploader = PhotoMessageUploader(m.ctx_api)
    random_photo_id = randint(1, 49)
    photo = await uploader.upload(
        file_source=f'bot/assets/images/pictures/{random_photo_id}.jpg',
        peer_id=m.peer_id,
    )

    # answer
    text = f'{ emojies.mount } { player.nickname }, Случайная картинка:'
    await m.answer(message=text, attachment=photo)