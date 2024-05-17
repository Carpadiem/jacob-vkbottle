from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.ledger} Профиль', payload={'action_type': 'button', 'action': 'show_profile'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.dollar_banknote} Деньги', payload={'action_type': 'button', 'action': 'show_money'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.bank} Банк', payload={'action_type': 'button', 'action': 'show_bank'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.desktop} Работы', payload={'action_type': 'button', 'action': 'show_jobs'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.briefcase} Бизнес', payload={'action_type': 'button', 'action': 'show_business'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.package} Кейсы', payload={'action_type': 'button', 'action': 'show_cases_shop'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.key} Имущество', payload={'action_type': 'button', 'action': 'show_my_property'}), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.reverse_button} Назад (Начало)', payload={'action_type': 'button', 'action': 'back_to_start'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()