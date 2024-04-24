from vkbottle import Keyboard, Text, KeyboardButtonColor

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'Помощь'), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'Основное'), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'Игры'), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'Другое'), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'MTA ресурсы'), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()