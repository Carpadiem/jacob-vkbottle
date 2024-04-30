# imports
from random import randint, randrange, choices
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
from vkbottle import BaseStateGroup
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity
from database.repository import Repository
# emojies
from emojies import emojies
# keyboard
from keyboards import keyboards
# tools
from tools import error_message, clear_current_state
# states
from config_states import my_state_dispenser
# utils
from utils.isNumber import isNumber
from utils.log import Log

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# player money = 100k
# all in (100k)
# 1/2 (50k)
# 1/3 (33.3k)
# 1/4 (25k)
# 1/8 (12.5k)
# text-number

# repos
playerRepo = Repository(entity=PlayerEntity())


# exit-handler
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'exit_casino' }))
async def exit_casino(m: Message):
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id }) # entities
    # answer
    text = f'{ emojies.slot_machine } { player.nickname }, Еще увидимся'
    await m.answer(message=text, keyboard=keyboards['games'])
    # clear state
    await clear_current_state(m)


# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'game_casino' }, text=['каз', 'казино']))
async def casino(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.slot_machine } { player.nickname }, Добро пожаловать в казино!
    
    { emojies.tip } У вас сейчас ${player.money:,} { emojies.dollar_banknote }
    { emojies.tip } Введите свою ставку или выберите её из меню:
    '''.replace('    ', '')
    await m.answer(message=text, keyboard=keyboards['game_casino'])
    # state dispenser set state
    await my_state_dispenser.set(m.peer_id, CasinoStates.BET_STATE)


class CasinoStates(BaseStateGroup):
    BET_STATE = 'casino_bet_state'


@bl.message(state=CasinoStates.BET_STATE)
async def state_bet_state(m: Message):
    
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })

    casino_bet = 0

    payload = m.get_payload_json()
    if payload != None:
        casino_bet = payload['casino_bet']
    else:
        # validation text-input
        if not isNumber(m.text):
            # error
            text = f'{ emojies.sparkles } { player.nickname }, Введите целое число, чтобы сделать ставку'
            await error_message(
                m=m,
                text=text,
            )
            return
        else:
            casino_bet = int(m.text)
        


    # play method
    async def play(bet: int):
        # check player money

        if player.money == 0:
            text = f'{ emojies.sparkles } У вас совсем не осталось денег ($0)'
            await error_message(
                m=m,
                text=text,
                keyboard=keyboards['games'],
            )
            await clear_current_state(m)
            return

        if bet > player.money:
            text = f'{ emojies.sparkles } Не хватает денег. У вас ${player.money:,} { emojies.dollar_banknote }'
            await error_message(
                m=m,
                text=text,
                keyboard=keyboards['game_casino'],
            )
            await clear_current_state(m)
            return
        else:
            # generate coefficient
            weights = [2, 20, 20, 5, 20, 20, 2]
            gen_coef = choices([0, .25, .5, 1, 2, 1.25, 5], weights=weights)[0]
            Log(f'gen_coef: {gen_coef}')
            # calculate result
            bet_multiply_on_coef: float = bet * gen_coef
            result = round(bet_multiply_on_coef - bet)

            # nothing
            if result == 0:
                text = f'''{ emojies.slot_machine } { player.nickname }, Результаты игры:
                
                { emojies.option } Ваша ставка: ${bet:,} { f"({payload['casino_bet']})" if payload != None else '' }
                { emojies.option } Коэффициент х{gen_coef}
                { emojies.option } Вы ничего не потеряли и не выиграли
                { emojies.option } Сейчас на руках: ${player.money:,} { emojies.dollar_banknote }
                '''.replace('    ', '')
                await m.answer(text)
                return
            # win
            elif result > 1:
                text = f'''{ emojies.slot_machine }{ emojies.checkmark } { player.nickname }, Результаты игры:
                
                { emojies.option } Ваша ставка: ${bet:,} { f"({payload['casino_bet']})" if payload != None else '' }
                { emojies.option } Коэффициент х{gen_coef}
                { emojies.option } Вы выиграли ${result:,} { emojies.dollar_banknote }
                { emojies.option } Сейчас на руках: ${player.money+result:,} { emojies.dollar_banknote }
                '''.replace('    ', '')
                await m.answer(text)
                await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + result })
                return
            # lose
            elif result < 1:
                text = f'''{ emojies.slot_machine }{ emojies.crossmark } { player.nickname }, Результаты игры:
                
                { emojies.option } Ваша ставка: ${bet:,} { f"({payload['casino_bet']})" if payload != None else '' }
                { emojies.option } Коэффициент х{gen_coef}
                { emojies.option } Вы потеряли ${abs(result):,} { emojies.dollar_banknote }
                { emojies.option } Сейчас на руках: ${player.money-abs(result):,} { emojies.dollar_banknote }
                '''.replace('    ', '')
                await m.answer(text)
                await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money - abs(result) })
                return


    # manual input (hand-text)
    if payload == None:
        await play(bet=casino_bet)

    # buttons input
    else:
        casino_bet: str = casino_bet
        if casino_bet == 'all-in':
            bet = player.money
            await play(bet)
        else: # 1/8, ...
            part_of = int(casino_bet.split('/')[1])
            bet = round(player.money / part_of)
            await play(bet)








# @bl.message(state=CasinoStates.BET_STATE)
# async def play_casino(m: Message):
#     # get payload from message
#     payload = m.get_payload_json()
#     casino_bet = payload['casino_bet']
#     # entities
#     player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })


# @bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'play_casino' }))
# async def play_casino(m: Message):
#     # get payload from message
#     payload = m.get_payload_json()
#     casino_bet = payload['casino_bet']
#     # entities
#     player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    
    

