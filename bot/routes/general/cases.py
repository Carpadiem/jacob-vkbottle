# imports
from random import choices, randrange
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
# rules
from rules import PayloadContainsOrTextRule
from vkbottle.dispatch.rules.base import PayloadContainsRule
# database
from database.repository import Repository
from database.entities import PlayerEntity
from database.entities import CasesEntity
# emojies
from emojies import emojies
# templates
from templates import templates
# game data
from constants import game_cases
# tools
from tools import error_message
from utils.log import Log

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
casesRepo = Repository(entity=CasesEntity())

# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_cases_shop' }, text=['кейсы', 'кейс']))
async def cases_shop(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    cases: CasesEntity = await casesRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'{ emojies.package } { player.nickname }, Меню кейсов:'
    template = templates['cases_shop'](counts=[cases.count_1, cases.count_2, cases.count_3, cases.count_4])
    await m.answer(message=text, template=template)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'buy_case' }))
async def buy_case(m: Message):
    
    # check price & player money
    # ...

    payload = m.get_payload_json()
    case_id = payload['case_id']
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    cases: CasesEntity = await casesRepo.find_one_by({ 'user_id': m.from_id })
    # check price & player money
    case_price = game_cases[case_id]['price']['amount']
    if player.money < case_price:
        # error message
        await error_message(m, f'{ emojies.sparkles } { player.nickname }, Не хватает денег. У вас: ${ player.money } { emojies.dollar_banknote }')
        return
    # update
    cases_json = cases.__dict__
    await casesRepo.update({ 'user_id': m.from_id }, { f'count_{case_id}': cases_json[f'count_{case_id}'] + 1 } )
    # answer
    text = f'''
    { emojies.package } { player.nickname }, Успешная покупка x1 { game_cases[case_id]["name"] }!
    '''.replace('    ', '')
    await m.answer(text)




@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'open_case' }))
async def open_case(m: Message):
    
    # check if player have case
    # start open case

    payload = m.get_payload_json()
    case_id = payload['case_id']
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    cases: CasesEntity = await casesRepo.find_one_by({ 'user_id': m.from_id })

    case_name = game_cases[case_id]['name']

    # check if player have case
    cases_json = cases.__dict__
    current_case_count = cases_json[f'count_{case_id}']
    if current_case_count < 1:
        # error message
        await error_message(m, f'{ emojies.sparkles } { player.nickname }, У вас 0 кейсов "{case_name}"')
        return
    
    # start open case
    game_case = game_cases[case_id]
    case_items = game_case['items']
    chances = [x['chance'] for x in case_items]
    random_item: dict = choices(case_items, chances)[0]

    item_type: str = random_item['item_type']
    item_amount: dict = random_item['amount']
    item_amount_min: int = item_amount['min']
    item_amount_max: int = item_amount['max']
    item_amount_step: int = item_amount['step']
    item_amount_result = randrange(item_amount_min, item_amount_max, item_amount_step)

    text = f'{ emojies.package } { player.nickname }, Вот что было внутри "{case_name}"\n\n'
    if item_type == 'money':
        text += f'{ emojies.option } ${item_amount_result:,} { emojies.dollar_banknote }'
        await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + item_amount_result })
    elif item_type == 'experience':
        text += f'{ emojies.option } Опыт {item_amount_result:,}'
        await playerRepo.update({ 'user_id': m.from_id }, { 'experience': player.experience + item_amount_result })
    elif item_type == 'special_currency':
        text += f'{ emojies.option } Спецвалюта {item_amount_result:,}'
        await playerRepo.update({ 'user_id': m.from_id }, { 'special_currency': player.special_currency + item_amount_result })

    # reduce case
    await casesRepo.update({ 'user_id': m.from_id }, { f'count_{case_id}': current_case_count - 1 })
    current_case_count = current_case_count - 1

    # open more button
    keyboard = None
    if current_case_count > 0:
        keyboard = Keyboard(one_time=False, inline=True)
        keyboard.add(Text(label=f'Открыть еще ({current_case_count} шт.)', payload={ 'action_type': 'button', 'action': 'open_case', 'case_id': case_id }), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()
        keyboard.add(Text(label=f'В магазин', payload={ 'action_type': 'button', 'action': 'show_cases_shop' }), color=KeyboardButtonColor.SECONDARY)
        keyboard = keyboard.get_json()
    else:
        keyboard = Keyboard(one_time=False, inline=True)
        keyboard.add(Text(label=f'В магазин', payload={ 'action_type': 'button', 'action': 'show_cases_shop' }), color=KeyboardButtonColor.SECONDARY)
        keyboard = keyboard.get_json()

    # answer
    await m.answer(message=text, keyboard=keyboard)