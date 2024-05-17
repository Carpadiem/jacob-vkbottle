from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

def func_keyboard(garage_slot: int, vehicle_game_id: int):
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add(Callback( label=f'{ emojies.reverse_button } Назад', payload={ 'action_type': 'callback_button', 'action': 'garage_select_slot', 'garage_slot': garage_slot, 'vehicle_game_id': vehicle_game_id }))
    keyboard = keyboard.get_json()
    return keyboard