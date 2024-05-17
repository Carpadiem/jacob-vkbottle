from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=True)
keyboard.add(Callback( label=f'{ emojies.reverse_button } Назад в гараж', payload={ 'action_type': 'callback_button', 'action': 'back_to_garage' }))
keyboard = keyboard.get_json()