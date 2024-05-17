from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

# cube
keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{ emojies.cube } 1', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 1 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cube } 2', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 2 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cube } 3', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 3 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.cube } 4', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 4 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cube } 5', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 5 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.cube } 6', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 6 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Назад (Игры)', payload={ 'action_type': 'button', 'action': 'show_games' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Назад (Начало)', payload={ 'action_type': 'button', 'action': 'back_to_start' }), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()