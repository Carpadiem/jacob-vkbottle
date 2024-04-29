from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{ emojies.scroll } Расклейщик листовок', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 1 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.blue_car } Автомеханик СТО', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 2 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.bellhop_bell } Официант в ресторане', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 3 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.tropical_drink } Директор ночного клуба', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 4 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.desktop } Веб-дизайнер', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 5 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.desktop } Разработчик', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 6 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.alien_monster } Кибербезопасник', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 7 }), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{ emojies.comet } Космический инженер', payload={ 'action_type': 'button', 'action': 'job_work', 'job_id': 8 }), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{ emojies.alien_monster } Назад (Основное)', payload={ 'action_type': 'button', 'action': 'show_general' }), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()