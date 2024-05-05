# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
from vkbottle import GroupEventType
from vkbottle.bot import MessageEvent
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback, ShowSnackbarEvent
# database
from database.repository import Repository
from database.entities import PlayerEntity, PropertyEntity
# emojies
from emojies import emojies
# const
from constants import game_property
# keyboards
from keyboards import keyboards
# utils
from utils.find_dict_in_list_by_prop import find_dict_in_list_by_prop
# tools
from tools import error_message, raw_event_error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
propertyRepo = Repository(entity=PropertyEntity())

# handlers
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_my_property' }))
async def show_my_property(m: Message):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    property: PropertyEntity = await propertyRepo.find_one_by({ 'user_id': m.from_id })
    
    player_phone = list(filter(lambda item: item['id'] == property.phone_id, game_property['phones']))
    player_computer = list(filter(lambda item: item['id'] == property.computer_id, game_property['computers']))
    player_tv = list(filter(lambda item: item['id'] == property.tv_id, game_property['tvs']))
    player_washing_machine = list(filter(lambda item: item['id'] == property.washing_machine_id, game_property['washing_machines']))
    player_shoes = list(filter(lambda item: item['id'] == property.shoes_id, game_property['shoes']))


    # answer
    text = f'''{ emojies.key } { player.nickname }, Ваше имущество:

    { emojies.option } Телефон: { player_phone[0]['name'] if len(player_phone) > 0 else 'Отсутствует' }
    { emojies.option } Компьютер: { player_computer[0]['name'] if len(player_computer) > 0 != None else 'Отсутствует' }
    { emojies.option } Телевизор: { player_tv[0]['name'] if len(player_tv) > 0 != None else 'Отсутствует' }
    { emojies.option } Стиральная машина: { player_washing_machine[0]['name'] if len(player_washing_machine) > 0 != None else 'Отсутствует' }
    { emojies.option } Тяги: { player_shoes[0]['name'] if len(player_shoes) > 0 != None else 'Отсутствует' }
    '''.replace('    ', '')
    await m.answer(message=text, keyboard=keyboards['goto_property_shop'])




@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'button', 'action': 'show_property_shop' }),
)
async def show_property_shop(event: MessageEvent):
    # payload
    payload = event.get_payload_json()
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': event.user_id })

    await event.edit_message(
        message=f'{ emojies.key } { player.nickname }, Магазин имущества:',
        keyboard=keyboards['property_shop']
    )








@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'button', 'action': 'property_shop_category' })
)
async def property_shop_category(event: MessageEvent):
    
    # payload
    payload = event.get_payload_json()
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': event.user_id })

    category = payload['category']
    keyboard = Keyboard(one_time=False, inline=True)
    counter = 0
    text = f''
    for item in game_property[category]:

        prop_name = item['name']
        prop_price_currency = item['price']['currency']
        prop_price_amount = item['price']['amount']
        prop_description = item['description']
        
        prop_price_text = ''
        if prop_price_currency == 'money':
            prop_price_text = f'${prop_price_amount:,}{ emojies.dollar_banknote }'
        else:
            pass

        text += f'''\
        { emojies.option } { item["id"] }. { prop_name } -- { prop_price_text }
        { emojies.scroll } { prop_description }

        '''.replace('    ', '')

        prop_payload_for_buy = {
            'action_type': 'button',
            'action': 'property_shop_buy',
            'category': category,
            'prop_id': item["id"],
            'price': item["price"] # includes { 'currency': ..., 'amount': ... }
        }

        keyboard.add(Callback(label=f'{ counter+1 }', payload=prop_payload_for_buy), color=KeyboardButtonColor.SECONDARY)
        # update counter
        counter += 1
        if counter % 5 == 0: keyboard.row()

    if keyboard.buttons[len(keyboard.buttons)-1] != []: keyboard.row()
    keyboard.add(Callback(label=f'{ emojies.reverse_button } Назад (Магазин)', payload={ 'action_type': 'button', 'action': 'show_property_shop' }), color=KeyboardButtonColor.SECONDARY)
    keyboard = keyboard.get_json()

    await event.edit_message(
        message=f'''{ emojies.key } { player.nickname },
        
        {text}

        { emojies.shopping_bags } Выберите номер, чтобы приобрести имущество:
        '''.replace('    ', ''),
        keyboard=keyboard
    )








@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'button', 'action': 'property_shop_buy' })
)
async def property_shop_buy(event: MessageEvent):

    # payload
    payload = event.get_payload_json()
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': event.user_id })

    answer_text = ''

    category = payload['category']
    prop_id = payload['prop_id']
    price = payload['price']

    # check player money (with price)
    if price['currency'] == 'money':
        player_money = player.money
        # error
        if player_money < price['amount']:
            text = f'{ emojies.sparkles } { player.nickname }, Не хватает денег. У вас: ${player.money:,}{ emojies.dollar_banknote }'
            keyboard = Keyboard(one_time=False, inline=True)
            keyboard.add(Callback(label=f'{ emojies.reverse_button } Назад (Магазин)', payload={ 'action_type': 'button', 'action': 'show_property_shop' }), color=KeyboardButtonColor.SECONDARY)
            keyboard = keyboard.get_json()
            await raw_event_error_message(event, text, keyboard)
            return
        # update player table
        await playerRepo.update({ 'user_id': event.user_id }, { 'money': player.money - price['amount'] })
        
        # answer text
        # find object in list by python-prop
        game_property_by_id = find_dict_in_list_by_prop(search_in=game_property[category], where={ 'id': prop_id })
        answer_text = f'{ emojies.shopping_bags } { player.nickname }, Вы приобрели { game_property_by_id["name"] } за ${price["amount"]:,} { emojies.dollar_banknote }'
        
    else:
        pass

    # update property table
    await propertyRepo.update({ 'user_id': event.user_id }, { 'phone_id': prop_id })
    
    # answer
    await event.edit_message(
        message=answer_text,
        keyboard=keyboards['property_shop']
    )