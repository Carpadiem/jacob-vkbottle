# imports
from math import ceil
from typing import List
import json
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import GroupEventType
from vkbottle.bot import MessageEvent
from vkbottle.dispatch.rules.base import PayloadContainsRule
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity, VehiclesEntity
from database.repository import Repository
# emojies
from emojies import emojies
# keyboards
from keyboards import keyboards
# consts
from constants import game_vehicles, max_vehicles_on_page
# utils
from utils.log import Log
from utils.is_number import is_number
from utils.find_dict_in_list_by_prop import find_dict_in_list_by_prop
# tools
from tools import error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True


# repos
playerRepo = Repository(entity=PlayerEntity())
vehiclesRepo = Repository(entity=VehiclesEntity())


async def show_autosalone_page(message_or_event: Message | MessageEvent, page: int):
    # get user id from Message type or Event type
    user_id = message_or_event.from_id if type(message_or_event) == Message else message_or_event.user_id
    # autosalon datas
    autosalone_vehicles_count = len(game_vehicles) # autosalone_vehicles_count
    autosalone_pages_count = ceil(autosalone_vehicles_count/max_vehicles_on_page) # calculate autosalone pages count
    # validation
    if not is_number(page):
        response = ('page_not_is_number')
        return response

    if page > autosalone_pages_count: page = 1
    elif page <= 0: page = autosalone_pages_count

    linestext = ''
    page_elements_counter = 0
    # cycle indicies
    start_element_index = page*max_vehicles_on_page-max_vehicles_on_page
    end_element_index = page*max_vehicles_on_page if start_element_index + len(game_vehicles) < page*max_vehicles_on_page else len(game_vehicles)
    # generate linestext
    for i in range(start_element_index, end_element_index):
        vehicle_id: int = game_vehicles[i]['id']
        brand: str = game_vehicles[i]['brand']
        model_name: str = game_vehicles[i]['model_name']
        price: int = game_vehicles[i]['price']
        description: str = game_vehicles[i]['description']
        specifications: dict = game_vehicles[i]['specifications']

        linestext += f'''\
        { emojies.option } { brand.capitalize() } { model_name.capitalize() } -- ${price:,} { emojies.dollar_banknote }        
        { emojies.symbol_id } ID: {vehicle_id}
        { emojies.acceleration } Характеристики:
        { emojies.max_speed } Скорость: { specifications['maxspeed'] } км/ч
        { emojies.acceleration } Ускорение: { specifications['acceleration'] } сек
        { emojies.control } Управляемость: { specifications['control'] }/10

        '''.replace('    ', '')

        page_elements_counter += 1
        if page_elements_counter == max_vehicles_on_page: break # max_vehicles_on_page = 5

    keyboard = keyboards['autosalone_pages_inline'](page, autosalone_pages_count)
    response = (linestext, keyboard)
    return response








# handlers
@bl.message(PayloadContainsOrTextRule(
    payload={ 'action_type': 'button', 'action': 'autosalone' },
    text='автосалон'
))
async def autosalone(m: Message, page=1):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # show autosalone page
    response = await show_autosalone_page(m, page)
    if response == ('page_not_is_number'):
        text = f'{ emojies.sparkles } { player.nickname }, Пример использования команды: Автосалон [страница]'
        await error_message(m, text)

    # answer
    text = f'''{ emojies.car } { player.nickname }, Автосалон:

    { response[0] }

    { emojies.tip } Приобрести: Автосалон купить [ID автомобиля]

    '''.replace('    ', '')
    await m.answer(message=text, keyboard=response[1])








@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'button', 'action': 'autosalone_change_page' })
)
async def autosalone_change_page(event: MessageEvent):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': event.user_id })
    # payload data
    payload = event.get_payload_json()
    page = payload['page']
    # show autosalone page
    response = await show_autosalone_page(event, page)
    # answer (callback edit)
    text = f'''{ emojies.car } { player.nickname }, Автосалон:

    { response[0] }

    { emojies.tip } Приобрести: Автосалон купить [ID автомобиля]
    '''.replace('    ', '')
    await event.edit_message(message=text, keyboard=response[1])







@bl.message(text=[
    'автосалон купить <vehicle_id>',
    'автосалон купить'
])
async def autosalone_purchase(m: Message, vehicle_id=None):

    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })

    # validation
    if not is_number(vehicle_id):
        text = f'{ emojies.sparkles } { player.nickname }, Пример использования команды: Автосалон купить [ID автомобиля: int]'
        await error_message(m, text)
        return
    
    # check if vehicle exist in autosalone
    vehicle_for_purchase = find_dict_in_list_by_prop(game_vehicles, { 'id': int(vehicle_id) })
    if vehicle_for_purchase == None:
        text = f'{ emojies.sparkles } { player.nickname }, В автосалоне нет транспорта с таким ID'
        await error_message(m, text)
        return
    
    # check if player hhave money
    vehicle_price = vehicle_for_purchase['price']
    if player.money < vehicle_price:
        text = f'{ emojies.sparkles } { player.nickname }, Не хватает денег. У вас ${player.money:,} { emojies.dollar_banknote }'
        await error_message(m, text)
        return
        
    # purchase vehicle & update player money
    vehicles: VehiclesEntity = await vehiclesRepo.find_one_by({ 'user_id': m.from_id })
    # load, update, dump
    json_vehicles: List[dict] = json.loads(vehicles.vehicles)
    json_vehicles.append(vehicle_for_purchase)
    json_vehicles = json.dumps(json_vehicles)
    # update vehicles in db
    await vehiclesRepo.update({ 'user_id': m.from_id }, { 'vehicles': json_vehicles })
    # update player money
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money - vehicle_price })

    # answer
    # build string vehicle name
    vehicle_name = ''
    vehicle_brand: str = vehicle_for_purchase['brand']
    vehicle_model_name: str = vehicle_for_purchase['model_name']
    vehicle_name = f'{ vehicle_brand.capitalize() } { vehicle_model_name.capitalize() }'
    text = f'''{ emojies.car } { player.nickname }, Приобретение { vehicle_name } за ${vehicle_price:,} { emojies.dollar_banknote }

    { emojies.tip } Новый транспорт ждет тебя в твоем гараже!
    '''.replace('    ', '')
    await m.answer(text)