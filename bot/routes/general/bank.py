# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import BaseStateGroup
from vkbottle.dispatch.rules.base import PayloadContainsRule
# rules
from rules import PayloadContainsOrTextRule
# keyboards
from keyboards import keyboards
# database
from database.entities import PlayerEntity, BankEntity
from database.repository import Repository
# emojies
from emojies import emojies
# states
# from ..bot import my_state_dispenser
from config_states import my_state_dispenser
# utils
from utils.isNumber import isNumber
from utils.log import Log
# tools
from tools import error_message, clear_current_state

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
bankRepo = Repository(entity=BankEntity())




# async def clear_current_state(m: Message):
#     current_state = await my_state_dispenser.get(m.peer_id)
#     if current_state != None: await my_state_dispenser.delete(m.peer_id)

# async def error_message(m: Message, text: str, keyboard=None, clear_state: bool=False):
#     await m.answer(message=text, keyboard=keyboard)
#     if clear_state:
#         await clear_current_state(m)




# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_bank' }, text='банк'))
async def money(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    bank: BankEntity = await bankRepo.find_one_by({ 'user_id': m.from_id })
    # keyboard
    keyboard = keyboards['bank']

    text = f'''{ emojies.bank } { player.nickname } , Банковский счет: ${bank.score:,} {emojies.dollar_banknote}

    { emojies.down_arrow } Пополнить: Банк пополнить
    { emojies.up_arrow } Пополнить: Банк снять
    { emojies.money_wings } Перевести игроку: Банк перевод
    '''.replace('    ', '')
    await m.answer(message=text, keyboard=keyboard)



# head handlers (text handlers)
# empty


# keyboard handler for cancel bank operations
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'bank_cancel' }))
async def bank_cancel(m: Message):
    # answer
    text = f'{ emojies.sparkles } Операция отменена'
    keyboard = keyboards['bank']
    await m.answer(message=text, keyboard=keyboard)
    await clear_current_state(m) # clear current state if exist




# keyboard-or-text handler
@bl.message(PayloadContainsOrTextRule(payload={'action_type': 'button', 'action': 'bank_push'}, text=['банк пополнить']))
async def bank_push_state(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.bank } { player.nickname }, Введите сумму для пополнения:'
    await m.answer(message=text, keyboard=keyboards['bank_cancel'])
    # set state
    await my_state_dispenser.set(m.peer_id, BankPushStates.BANK_PUSH_STATE, payload={ 'player': player })

# state handler
class BankPushStates(BaseStateGroup):
    BANK_PUSH_STATE = 'bank_push_state'

@bl.message(state=BankPushStates.BANK_PUSH_STATE)
async def state_bank_push_state(m: Message):
    # get player from payload
    payload = m.state_peer.payload['payload']
    player: PlayerEntity = payload['player']
    # args validation
    amount = m.text
    if not isNumber(amount):
        # error message
        await error_message(m=m, text=f'{ emojies.sparkles } { player.nickname }, Укажите целое число', keyboard=keyboards['bank'])
        await clear_current_state(m)
        return
    # update bank score
    bank: BankEntity = await bankRepo.find_one_by({ 'user_id': m.from_id })
    if player.money < int(amount): # check player money
        # error message
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Не хватает денег. У вас: ${ player.money:, } { emojies.dollar_banknote }',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return
    # update
    await bankRepo.update({ 'user_id': m.from_id }, { 'score': bank.score + int(amount) })
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money - int(amount) })
    # answer
    text = f'{ emojies.checkmark } { player.nickname }, Успешное пополнение счета на ${int(amount):,} { emojies.dollar_banknote }'
    await m.answer(message=text, keyboard=keyboards['bank'])
    # clear current state
    await clear_current_state(m)




# keyboard-or-text handler
@bl.message(PayloadContainsOrTextRule(payload={'action_type': 'button', 'action': 'bank_pull'}, text=['банк снять']))
async def bank_pull_state(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.bank } { player.nickname }, Введите сумму для снятия:'
    await m.answer(message=text, keyboard=keyboards['bank_cancel'])
    # set state
    await my_state_dispenser.set(m.peer_id, BankPullStates.BANK_PULL_STATE, payload={ 'player': player })

# state handler
class BankPullStates(BaseStateGroup):
    BANK_PULL_STATE = 'bank_pull_state'

@bl.message(state=BankPullStates.BANK_PULL_STATE)
async def state_bank_pull_state(m: Message):
    # get player from payload
    payload = m.state_peer.payload['payload']
    player: PlayerEntity = payload['player']
    # args validation
    amount = m.text
    if not isNumber(amount):
        # error message
        await error_message(m=m, text=f'{ emojies.sparkles } { player.nickname }, Укажите целое число', keyboard=keyboards['bank'], clear_state=True)
        return
    # update bank score
    bank: BankEntity = await bankRepo.find_one_by({ 'user_id': m.from_id })
    if bank.score < int(amount): # check bank score
        # error message
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Недостаточно на счете. У вас: ${bank.score:,} { emojies.dollar_banknote }',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return
    # update
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + int(amount) })
    await bankRepo.update({ 'user_id': m.from_id }, { 'score': bank.score - int(amount) })
    # answer
    text = f'{ emojies.checkmark } { player.nickname }, Успешное снятия со счета ${int(amount):,} { emojies.dollar_banknote }'
    await m.answer(message=text, keyboard=keyboards['bank'])
    # clear current state
    await clear_current_state(m)




# keyboard-or-text handler
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'bank_transfer' }, text=['банк перевод']))
async def bank_transfer(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.bank } { player.nickname }, Введите игровой ID игрока и сумму через пробел:'
    await m.answer(message=text, keyboard=keyboards['bank_cancel'])
    # set state
    await my_state_dispenser.set(m.peer_id, BankTransferStates.BANK_TRANSFER_STATE, payload={ 'player': player })

# state handler
class BankTransferStates(BaseStateGroup):
    BANK_TRANSFER_STATE = 'bank_transfer_state'

@bl.message(state=BankTransferStates.BANK_TRANSFER_STATE)
async def state_bank_transfer_state(m: Message):
    # get player from payload
    payload = m.state_peer.payload['payload']
    player: PlayerEntity = payload['player']
    # get args
    args = m.text.split(' ')
    recipient_id = args[0]
    amount = args[1]
    # validation
    if not isNumber(recipient_id):
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Укажите игровой ID игрока как целое число',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return
    if not isNumber(recipient_id):
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Укажите сумму перевода как целое число',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return
    
    # try find recipient
    # (?) check transfers limit
    # check sender bank.score
    # try transfer (sender > recipient)
    # update recipient's & sender's money & bank score

    # try find recipient from db
    recipient_bank: BankEntity = await bankRepo.find_one_by({ 'player_id': recipient_id })
    if recipient_bank == None:
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Игрока с таким ID нет',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return
    
    # check sender bank score
    sender_bank: BankEntity = await bankRepo.find_one_by({ 'user_id': m.from_id })
    if sender_bank.score < int(amount):
        await error_message(
            m=m,
            text=f'{ emojies.sparkles } { player.nickname }, Недостаточно средств. Ваш счет: ${int(amount):,} {emojies.dollar_banknote}',
            keyboard=keyboards['bank'],
        )
        await clear_current_state(m)
        return

    # try make transfer
    await bankRepo.update({ 'user_id': m.from_id }, { 'score': sender_bank.score - int(amount) }) # sender bank.score update
    await bankRepo.update({ 'player_id': recipient_id }, { 'score': recipient_bank.score + int(amount) }) # recipient bank.score update

    # answer
    recipient: PlayerEntity = await playerRepo.find_one_by({ 'player_id': recipient_id })
    # answer sender
    text = f'{ emojies.checkmark } { player.nickname }, Успешный перевод ${int(amount):,} { emojies.dollar_banknote} игроку @id{recipient.user_id}({ recipient.nickname })'
    await m.answer(message=text, keyboard=keyboards['bank'])
    # answer recipient
    text = f'{ emojies.bank } { recipient.nickname }, Входящий перевод ${int(amount):,} { emojies.dollar_banknote} от @id{player.user_id}({ player.nickname })'
    await m.ctx_api.messages.send(
        user_id=recipient.user_id,
        peer_id=recipient.user_id,
        random_id=0,
        message=text,
    )
    # clear current state
    await clear_current_state(m)