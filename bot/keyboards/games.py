from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

# games
keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.cube} Кубик', payload={'action_type': 'button', 'action': 'game_cube'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.cup} Стакан', payload={'action_type': 'button', 'action': 'game_cup'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.slot_machine} Казино', payload={'action_type': 'button', 'action': 'game_casino'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.reverse_button} Назад (Начало)', payload={'action_type': 'button', 'action': 'back_to_start'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()

# cube
keyboard_game_cube = Keyboard(one_time=False, inline=False)
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 1', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 1 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 2', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 2 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 3', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 3 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.row()
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 4', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 4 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 5', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 5 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.add(Text(label=f'{ emojies.cube } 6', payload={ 'action_type': 'button', 'action': 'play_cube', 'cube_number': 6 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.row()
keyboard_game_cube.add(Text(label=f'{ emojies.reverse_button } Назад (Игры)', payload={ 'action_type': 'button', 'action': 'show_games' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube.row()
keyboard_game_cube.add(Text(label=f'{ emojies.reverse_button } Назад (Начало)', payload={ 'action_type': 'button', 'action': 'back_to_start' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cube = keyboard_game_cube.get_json()

# cup
keyboard_game_cup = Keyboard(one_time=False, inline=False)
keyboard_game_cup.add(Text(label=f'{ emojies.cup } 1', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 1 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cup.add(Text(label=f'{ emojies.cup } 2', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 2 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cup.add(Text(label=f'{ emojies.cup } 3', payload={ 'action_type': 'button', 'action': 'play_cup', 'cup_number': 3 }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cup.row()
keyboard_game_cup.add(Text(label=f'{ emojies.reverse_button } Назад (Игры)', payload={ 'action_type': 'button', 'action': 'show_games' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cup.row()
keyboard_game_cup.add(Text(label=f'{ emojies.reverse_button } Назад (Начало)', payload={ 'action_type': 'button', 'action': 'back_to_start' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_cup = keyboard_game_cup.get_json()

# casino
keyboard_game_casino = Keyboard(one_time=False, inline=False)
keyboard_game_casino.add(Text(label=f'1/8', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/8' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino.add(Text(label=f'1/4', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/4' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino.row()
keyboard_game_casino.add(Text(label=f'1/3', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/3' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino.add(Text(label=f'1/2', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/2' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino.row()
keyboard_game_casino.add(Text(label=f'All-In', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': 'all-in' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino.row()
keyboard_game_casino.add(Text(label=f'{ emojies.reverse_button } Выход', payload={ 'action_type': 'button', 'action': 'exit_casino' }), color=KeyboardButtonColor.SECONDARY)
keyboard_game_casino = keyboard_game_casino.get_json()