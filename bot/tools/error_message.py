from vkbottle.bot import Message
from tools import clear_current_state

async def error_message(m: Message, text: str, keyboard=None, clear_state: bool=False):
    await m.answer(message=text, keyboard=keyboard)
    if clear_state:
        await clear_current_state(m)