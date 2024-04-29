# imports
from math import floor
# vkbottle
from vkbottle.bot import BotLabeler, Message
# rules
from rules import PayloadContainsOrTextRule
from vkbottle.dispatch.rules.base import PayloadContainsRule
# database
from database.repository import Repository
from database.entities import PlayerEntity, BusinessEntity
# emojies
from emojies import emojies
# templates
from templates import templates
# keyboard
from keyboards import keyboards
# game data
from constants import game_cases
# tools
from tools import error_message
from utils.log import Log
from utils.ts_now import ts_now
# constants
from constants import game_businesses

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
businessRepo = Repository(entity=BusinessEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_business' }, text=['бизнес', 'бизнесы']))
async def business_menu(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.briefcase } { player.nickname }, Выберите действие из меню:'
    await m.answer(message=text, keyboard=keyboards['business'])




PROFIT_MINUTES_DIVIDER = 60
def calculate_profit(ts_previous_profit: int, earnings_per_hour: int) -> int:
    diff_seconds = ts_now() - ts_previous_profit
    diff_in_mins = diff_seconds / 60
    total_profit_cycles_by_each_hour = diff_in_mins / PROFIT_MINUTES_DIVIDER 
    result_profit = int(earnings_per_hour * floor(total_profit_cycles_by_each_hour))
    return result_profit




@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_my_business' }, text=['мой бизнес']))
async def show_my_business(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    business: BusinessEntity = await businessRepo.find_one_by({ 'user_id': m.from_id })
    # if player's business_id is 0
    if business.business_id == 0:
        await error_message(m, f'{ emojies.sparkles } { player.nickname }, У вас нет бизнеса')
        return
    # calculate_profit
    game_business = game_businesses[business.business_id]
    earnings_per_hour = game_business['options']['earnings_per_hour']
    collected_profit = calculate_profit(business.ts_previous_profit, earnings_per_hour=earnings_per_hour)
    # answer
    text = f'''{ emojies.briefcase } { player.nickname }, Статистика "{ game_business['name'] }":

    { emojies.money_wings } Доход/час: {earnings_per_hour:,}$
    { emojies.money_bag } Накопленная прибыль: {collected_profit:,}$
    '''.replace('    ', '')
    await m.answer(message=text, keyboard=keyboards['my_business'])




@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'business_shop' }, text=['бизнесы','магазин бизнесов']))
async def business_shop(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.briefcase } { player.nickname }, Магазин бизнесов:'
    template = templates['businesses_shop']
    await m.answer(message=text, template=template)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'buy_business' }))
async def buy_business(m: Message):
    payload = m.get_payload_json()
    purchased_business_id = payload['business_id']
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    business: BusinessEntity = await businessRepo.find_one_by({ 'user_id': m.from_id })
    # check if business exist
    if business.business_id != 0:
        name = game_businesses[business.business_id]['name']
        await error_message(m, f'{ emojies.sparkles } { player.nickname }, У вас уже есть бизнес "{name}"')
        return
    purchased_business_price = game_businesses[purchased_business_id]['price']
    if player.money < purchased_business_price:
        await error_message(m, f'{ emojies.sparkles } { player.nickname }, Не хватает денег. У вас ${player.money:,} { emojies.dollar_banknote }')
        return
    # reduce money
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money - purchased_business_price })
    # update business repo (business_id=purchased_business_id, ts_previous_profit=ts_now)
    await businessRepo.update({ 'user_id': m.from_id }, { 'business_id': purchased_business_id })
    await businessRepo.update({ 'user_id': m.from_id }, { 'ts_previous_profit': ts_now() })
    # answer
    purchased_business_name = game_businesses[purchased_business_id]['name']
    text = f'{ emojies.briefcase } { player.nickname }, Вы приобрели "{purchased_business_name}" за ${purchased_business_price:,} { emojies.dollar_banknote }'
    await m.answer(message=text, keyboard=keyboards['my_business'])




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'business_profit' }))
async def business_profit(m: Message):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    business: BusinessEntity = await businessRepo.find_one_by({ 'user_id': m.from_id })
    # calculate collected profit
    player_business_info = game_businesses[business.business_id]
    earnings_per_hour = player_business_info['options']['earnings_per_hour']
    result_profit = calculate_profit(business.ts_previous_profit, earnings_per_hour)
    # if collected profit is zero
    if result_profit == 0:
        text = f'''{ emojies.sparkles } { player.nickname }, На счете бизнеса пока что 0$ { emojies.dollar_banknote }

        { emojies.tip } Прибыль приходит каждый час
        '''.replace('    ', '')
        await error_message(m, text)
        return
    
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + result_profit }) # update player's money
    await businessRepo.update({ 'user_id': m.from_id }, { 'ts_previous_profit': ts_now() }) # update player's business profit ts_previous_profit
    # answer
    text = f'''{ emojies.briefcase } { player.nickname }, Прибыль ${result_profit:,} { emojies.dollar_banknote }'''
    await m.answer(text)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'business_sell' }))
async def business_sell(m: Message):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    business: BusinessEntity = await businessRepo.find_one_by({ 'user_id': m.from_id })
    # check if player have business
    if business.business_id == 0:
        text = f'''{ emojies.sparkles } { player.nickname }, У вас нет бизнеса
        
        { emojies.tip } Приобрести: Бизнес
        '''.replace('    ', '')
        await error_message(m, text)
        return
    
    business_price = game_businesses[business.business_id]['price']
    business_price_for_sell = round(business_price / 2)

    # update business table (set business_id = 0)
    await businessRepo.update({ 'user_id': m.from_id }, { 'business_id': 0 })
    # update player's money (set money = money + business_price_for_sell)
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + business_price_for_sell })

    # answer
    business_name = game_businesses[business.business_id]['name']
    text = f'{ emojies.briefcase } Вы продали "{ business_name }" за ${business_price_for_sell:,} { emojies.dollar_banknote }'
    await m.answer(message=text, keyboard=keyboards['business'])



