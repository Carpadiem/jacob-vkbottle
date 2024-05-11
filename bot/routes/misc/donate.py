# imports
from random import randint
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
from rules import PayloadContainsOrTextRule
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
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'donate' }, text=['донат']))
async def donate(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.gem_stone } { player.nickname }, Какой вид доната интересует?'
    await m.answer(message=text, keyboard=keyboards['donate'])




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'donate_currency' }))
async def donate_currency(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.option } { player.nickname }, Информация по валютному донату:

    { emojies.orange_diamond } 100,000 GC - 20 RUB
    { emojies.orange_diamond } 250,000 GC - 50 RUB
    { emojies.orange_diamond } 600,000 GC - 96 RUB (20% скидка)
    { emojies.orange_diamond } 1,500,000 GC - 160 RUB (20% скидка)

    { emojies.info } GC - игровая валюта ($)

    { emojies.orange_diamond } X2 опыт на 24 часа - 10 RUB
    { emojies.orange_diamond } X2 заработок 24 часа - 20 RUB
    { emojies.orange_diamond } X2 скорость восстановления энергии на 24 часа - 10 RUB

    { emojies.orange_diamond } Запас энергии 30 на 24 часа - 15 RUB
    { emojies.orange_diamond } Запас энергии 50 на 24 часа - 20 RUB

    { emojies.info } Если у вас большой запас энергии, рекомендуем взять в комплект "Скорость восстановления энергии х2"

    { emojies.info } При покупке любой опции из категории "Энергия", ваша энергия пополнится до своего максимального количества

    { emojies.comet } Если хотите приобрести донат (сделать пожертвование в обмен на предметы и привилегии в игре), нажмите на кнопку "Хочу поддержать" в меню ниже.
    '''.replace('    ', '')
    await m.answer(text)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'donate_privilege' }))
async def donate_currency(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.gem_stone } { player.nickname }, Информация по привилегиям:

    { emojies.orange_diamond } 𝗘𝗹𝗶𝘁𝗲 - 𝟰𝟬 𝗥𝗨𝗕
    ⠀⠀- Удвоенный ежедневный бонус
    ⠀⠀- Возможность написать игроку
    ⠀⠀- Возможность посмотреть профиль игрока

    { emojies.orange_diamond } 𝗣𝗿𝗼 - 𝟳𝟬 𝗥𝗨𝗕
    ⠀⠀- Удвоенный ежедневный бонус
    ⠀⠀- X2 опыт
    ⠀⠀- Скорость восстановления энергии х2

    { emojies.orange_diamond } 𝗪𝗮𝘁𝗰𝗵𝗲𝗿 - 𝟭𝟱𝟬 𝗥𝗨𝗕
    ⠀⠀- Удвоенный ежедневный бонус
    ⠀⠀- X2 заработок
    ⠀⠀- Запас энергии 30

    { emojies.orange_diamond } 𝗘𝘅𝗽𝗹𝗼𝗿𝗲𝗿 - 𝟭𝟳𝟱 𝗥𝗨𝗕
    ⠀⠀- Удвоенный ежедневный бонус
    ⠀⠀- X2 опыт
    ⠀⠀- X2 заработок
    ⠀⠀- Запас энергии 50
    ⠀⠀- Скорость восстановления энергии х2

    { emojies.comet } Если хотите приобрести донат (сделать пожертвование в обмен на предметы и привилегии в игре), нажмите на кнопку "Хочу поддержать" в меню ниже.
    '''.replace('    ', '')
    await m.answer(text)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'donate_donation' }))
async def donate_donation(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.like } Спасибо за проявленный интерес к игре и желание помочь в развитии!

    { emojies.watch } { player.nickname }, Ожидайте связи в течении 30 минут
    '''.replace('    ', '')
    await m.answer(text)

    # answer to manager
    manager_text = f'{ emojies.gem_stone } @id{m.from_id}(Пользователь) создал заявку на приобретение доната'
    await m.ctx_api.messages.send(
        user_id=230990098,
        peer_id=230990098,
        random_id=0,
        message=manager_text,
    )