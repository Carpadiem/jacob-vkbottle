from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

def func_keyboard(garage_slot: int, vehicle_game_id: int):
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add(Callback(label=f'{ emojies.hammer_and_wrench } Стайлинг', payload={ 'action_type': 'callback_button', 'action': 'garage_styling', 'garage_slot': garage_slot, 'vehicle_game_id': vehicle_game_id }))
    keyboard.row()
    keyboard.add(Callback(label=f'{ emojies.reverse_button } Назад в гараж', payload={ 'action_type': 'callback_button', 'action': 'back_to_garage' }))
    keyboard = keyboard.get_json()
    return keyboard