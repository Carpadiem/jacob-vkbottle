# imports
import json
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import GroupEventType, EMPTY_KEYBOARD, PhotoMessageUploader
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




def get_player_vehicles(user_id: int) -> list:
    # entities
    vehicles: VehiclesEntity = vehiclesRepo.find_one_by({ 'user_id': user_id })
    player_vehicles: list = json.loads(vehicles.vehicles)
    return player_vehicles




# handlers
@bl.message(PayloadContainsOrTextRule(
    payload={ 'action_type': 'button', 'action': 'my_garage' },
    text='гараж'
))
async def my_garage(m: Message):    
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })
    
    # player_vehicles_list
    player_vehicles_list = get_player_vehicles(m.from_id)
    
    # answer
    if len(player_vehicles_list) > 0:
        text = f'{ emojies.blue_car } { player.nickname }, В вашем гараже:'
        await m.answer(message=text, keyboard=keyboards['player_vehicles_inline'](player_vehicles_list))
    else:
        text = f'''{ emojies.blue_car } { player.nickname }, В вашем гараже нет автомобилей

        { emojies.tip } Посетите автосалон, чтобы приобрести новый транспорт
        '''.replace('    ', '')
        await m.answer(message=text)








@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'callback_button', 'action': 'garage_select_slot' })
)
async def garage_select_slot(event: MessageEvent):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': event.user_id })
    # payload data
    payload = event.get_payload_json()
    garage_slot = payload['garage_slot']
    vehicle_game_id = payload['vehicle_game_id']

    # get vehicle as game-object

    game_vehicle = find_dict_in_list_by_prop(search_in=game_vehicles, where={ 'id': vehicle_game_id })
    # build vehicle name
    vehicle_brand: str = game_vehicle['brand']
    vehicle_model_name: str = game_vehicle['model_name']
    vehicle_name = f'{ vehicle_brand.capitalize() } { vehicle_model_name.capitalize() }'
    # get vehicle specifications
    vehicle_maxspeed = game_vehicle['specifications']['maxspeed']
    vehicle_acceleration = game_vehicle['specifications']['acceleration']
    vehicle_control = game_vehicle['specifications']['control']

    # uploader
    uploader = PhotoMessageUploader(event.ctx_api)
    photo = await uploader.upload(
        file_source=f'bot/assets/images/vehicles/{vehicle_brand.lower()}_{vehicle_model_name.lower()}.jpg',
        peer_id=event.peer_id,
    )

    # answer (callback edit)
    text = f'''{ emojies.car } { player.nickname }, Ваш {vehicle_name}:

    { emojies.symbol_id } Номера слота в гараже: { garage_slot }
    
    { emojies.max_speed } Скорость: { vehicle_maxspeed } км/ч
    { emojies.acceleration } Разгон: { vehicle_acceleration } сек.
    { emojies.control } Управляемость: { vehicle_control }/10

    { emojies.tip } Продать: Гараж продать { garage_slot }
    '''.replace('    ', '')
    await event.edit_message(message=text, attachment=photo, keyboard=keyboards['vehicle_by_slot'](garage_slot, vehicle_game_id))




@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'callback_button', 'action': 'garage_styling' })
)
async def garage_styling(event: MessageEvent):

    # payload
    payload = event.get_payload_json()
    garage_slot = payload['garage_slot']
    vehicle_game_id = payload['vehicle_game_id']

    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': event.user_id })

    text = f'''{ emojies.hammer_and_wrench } { player.nickname }, Добро пожаловать в сервис стайлинга автомобилей JacobCustoms!

    { emojies.fire } Чтобы заниматься стайлингом своих автомобилей, перейдите на сайт игры: https://jacobgame.ru
    
    { emojies.tip } Другая дополнительная информация и помощь по стайлингу также находится на сайте игры. Удачи!
    '''.replace('    ', '')
    await event.edit_message(message=text, keyboard=keyboards['garage_styling_inline'](garage_slot, vehicle_game_id))




@bl.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
    PayloadContainsRule({ 'action_type': 'callback_button', 'action': 'back_to_garage' })
)
async def back_to_garage(event: MessageEvent):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': event.user_id })

    # player_vehicles_list
    player_vehicles_list = get_player_vehicles(event.user_id)

    # answer
    if len(player_vehicles_list) > 0:
        text = f'{ emojies.blue_car } { player.nickname }, В вашем гараже:'
        await event.edit_message(message=text, keyboard=keyboards['player_vehicles_inline'](player_vehicles_list))
    else:
        text = f'''{ emojies.blue_car } { player.nickname }, В вашем гараже нет автомобилей

        { emojies.tip } Посетите автосалон, чтобы приобрести новый транспорт
        '''.replace('    ', '')
        await event.edit_message(message=text, keyboard=EMPTY_KEYBOARD)




@bl.message(text='гараж продать <garage_slot>')
async def sell_vehicle(m: Message, garage_slot=None):
    # entities
    player: PlayerEntity = playerRepo.find_one_by({ 'user_id': m.from_id })

    # validation
    if not is_number(garage_slot) or int(garage_slot) < 0:
        text = f'{ emojies.sparkles } { player.nickname }, Пример использования команды: Гараж продать [номер слота]'
        await error_message(m, text)
        return

    player_vehicles: list = get_player_vehicles(m.from_id)
    if len(player_vehicles) <= 0:
        text = f'{ emojies.sparkles } { player.nickname }, В вашем гараже нет транспортных средств'
        await error_message(m, text)
        return
    
    vehicle_for_sell = None
    try:
        vehicle_for_sell = player_vehicles[int(garage_slot)-1]
    except IndexError:
        text = f'{ emojies.sparkles } { player.nickname }, Это свободный слот. Здесь у вас нет транспортных средств'
        await error_message(m, text)
        return

    price: int = vehicle_for_sell['price']
    sell_price = round(price - price / 3)

    # db updates
    # update money (add)
    playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + sell_price })

    # update vehicles
    vehicles: VehiclesEntity = vehiclesRepo.find_one_by({ 'user_id': m.from_id })
    vehicles_json: list = json.loads(vehicles.vehicles)
    vehicles_json.pop(int(garage_slot)-1)
    vehicles_dumped = json.dumps(vehicles_json)
    vehiclesRepo.update({ 'user_id': m.from_id }, { 'vehicles': vehicles_dumped })

    # get vehicle name
    vehicle_name = str(vehicle_for_sell['brand']).capitalize() + str(vehicle_for_sell['model_name']).capitalize()

    # answer
    text = f'{ emojies.blue_car } { player.nickname }, Вы продали "{ vehicle_name }" за ${sell_price:,} { emojies.dollar_banknote }'
    await m.answer(text)


