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