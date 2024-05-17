from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

# casino
keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'1/8', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/8' }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'1/4', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/4' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'1/3', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/3' }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'1/2', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': '1/2' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'All-In', payload={ 'action_type': 'button', 'action': 'play_casino', 'casino_bet': 'all-in' }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.reverse_button } Выход', payload={ 'action_type': 'button', 'action': 'exit_casino' }), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()