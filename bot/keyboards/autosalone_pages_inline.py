from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

def func(current_page: int, max_pages: int):
    keyboard = Keyboard(one_time=False, inline=True)
    keyboard.add(Callback(label=f'{ emojies.left_arrow }', payload={ 'action_type': 'button', 'action': 'autosalone_change_page', 'page': current_page-1 }), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text(label=f'{current_page}/{max_pages}'), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Callback(label=f'{ emojies.right_arrow }', payload={ 'action_type': 'button', 'action': 'autosalone_change_page', 'page': current_page+1 }), color=KeyboardButtonColor.SECONDARY)
    keyboard = keyboard.get_json()
    return keyboard
