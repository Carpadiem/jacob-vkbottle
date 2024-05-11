from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.bellhop_bell} Помощь', payload={'action_type': 'button', 'action': 'show_help'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.alien_monster} Основное', payload={'action_type': 'button', 'action': 'show_general'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.cube} Игры', payload={'action_type': 'button', 'action': 'show_games'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.mount} Другое', payload={'action_type': 'button', 'action': 'show_misc'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.car} Автотранспорт', payload={'action_type': 'button', 'action': 'motor_transport'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()