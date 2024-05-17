from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{ emojies.briefcase } Мой бизнес', payload={'action_type': 'button', 'action': 'show_my_business'}), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.money_bag } Приобрести бизнес', payload={'action_type': 'button', 'action': 'business_shop'}), color=KeyboardButtonColor.POSITIVE)
keyboard.row()
keyboard.add(Text(label=f'{emojies.alien_monster} Назад (Основное)', payload={'action_type': 'button', 'action': 'show_general'}), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()

keyboard_my_business = Keyboard(one_time=False, inline=False)
keyboard_my_business.add(Text(label=f'{ emojies.briefcase } Статистика', payload={ 'action_type': 'button', 'action': 'show_my_business' }), color=KeyboardButtonColor.SECONDARY)
keyboard_my_business.row()
keyboard_my_business.add(Text(label=f'{ emojies.money_bag } Получить прибыль', payload={ 'action_type': 'button', 'action': 'business_profit' }), color=KeyboardButtonColor.SECONDARY)
keyboard_my_business.add(Text(label=f'{ emojies.dollar_banknote } Продать бизнес', payload={ 'action_type': 'button', 'action': 'business_sell' }), color=KeyboardButtonColor.SECONDARY)
keyboard_my_business.row()
keyboard_my_business.add(Text(label=f'{ emojies.reverse_button } Назад (Бизнес)', payload={ 'action_type': 'button', 'action': 'show_business' }), color=KeyboardButtonColor.SECONDARY)
keyboard_my_business.row()
keyboard_my_business.add(Text(label=f'{ emojies.reverse_button } Назад (Основное)', payload={ 'action_type': 'button', 'action': 'show_general' }), color=KeyboardButtonColor.SECONDARY)
keyboard_my_business = keyboard_my_business.get_json()