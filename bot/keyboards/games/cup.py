from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

# cup
keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{ emojies.cup } 1', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 1 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cup } 2', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 2 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cup } 3', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 3 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Назад (Игры)', payload={ 'action_type': 'button', 'action': 'show_games' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Назад (Начало)', payload={ 'action_type': 'button', 'action': 'back_to_start' }), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()