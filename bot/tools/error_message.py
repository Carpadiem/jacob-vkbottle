from vkbottle.bot import Message

async def error_message(m: Message, text: str, keyboard=None):
    await m.answer(message=text, keyboard=keyboard)