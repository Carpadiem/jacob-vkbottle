from vkbottle import Keyboard, Text, KeyboardButtonColor
from emojies import emojies

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label=f'{emojies.bellhop_bell} Помощь'), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.ledger} Основное'), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.cube} Игры'), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text(label=f'{emojies.mount} Другое'), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text(label=f'{emojies.video_game} MTA ресурсы'), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()