from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{ emojies.car } Автосалон', payload={ 'action_type': 'button', 'action': 'autosalone' }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.blue_car } Мой гараж', payload={ 'action_type': 'button', 'action': 'my_garage' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Назад (Начало)', payload={ 'action_type': 'button', 'action': 'back_to_start' }), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()