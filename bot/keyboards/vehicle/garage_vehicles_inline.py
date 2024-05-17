from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

def func_keyboard(player_vehicles: list):
    keyboard = Keyboard(one_time=False, inline=True)
    
    garage_slot = 0
    for vehicle in player_vehicles:
        
        # increment garage slot
        garage_slot += 1
        
        # build vehicle name
        player_vehicle_brand: str = vehicle['brand']
        player_vehicle_model_name: str = vehicle['model_name']
        player_vehicle_name = f'{ player_vehicle_brand.capitalize() } { player_vehicle_model_name.capitalize() }'

        # get vehicle game id from player_vehicles
        vehicle_game_id = vehicle['id']
        
        keyboard.add(Callback(label=f'{ emojies.option } { player_vehicle_name }', payload={ 'action_type': 'button', 'action': 'garage_select_vehicle', 'garage_slot': garage_slot, 'vehicle_game_id': vehicle_game_id }), color=KeyboardButtonColor.SECONDARY)
        keyboard.row()

    keyboard.buttons.pop()
    keyboard = keyboard.get_json()
    return keyboard
