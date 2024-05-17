from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.down_arrow} Пополнить', payload={'action_type': 'button', 'action': 'bank_push'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.up_arrow} Снять', payload={'action_type': 'button', 'action': 'bank_pull'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.money_wings} Перевести игроку', payload={'action_type': 'button', 'action': 'bank_transfer'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.reverse_button} Назад (Основное)', payload={'action_type': 'button', 'action': 'show_general'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()

keyboard_cancel = Keyboard(one_time=False, inline=False)
keyboard_cancel.add(Text(label=f'Отмена', payload={'action_type': 'button', 'action': 'bank_cancel'}), color=KeyboardButtonColor.NEGATIVE)
keyboard_cancel = keyboard_cancel.get_json()