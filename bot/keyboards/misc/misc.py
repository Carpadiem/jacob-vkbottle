from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.mount} Пикча', payload={'action_type': 'button', 'action': 'picture'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.gem_stone} Донат', payload={'action_type': 'button', 'action': 'donate'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.red_triangle} Репорт', payload={'action_type': 'button', 'action': 'report'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.reverse_button} Назад (Начало)', payload={'action_type': 'button', 'action': 'back_to_start'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()