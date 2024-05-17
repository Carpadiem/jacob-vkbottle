from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.dollar_banknote} Валютный', payload={'action_type': 'button', 'action': 'donate_currency'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.gem_stone} Привилегия', payload={'action_type': 'button', 'action': 'donate_privilege'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.like} Хочу поддержать', payload={'action_type': 'button', 'action': 'donate_donation'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.reverse_button} Назад (Другое)', payload={'action_type': 'button', 'action': 'show_misc'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()