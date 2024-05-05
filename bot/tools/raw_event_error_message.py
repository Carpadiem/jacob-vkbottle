from vkbottle.bot import MessageEvent

async def raw_event_error_message(event: MessageEvent, text: str, keyboard=None):
    await event.send_message(
        message=text,
        keyboard=keyboard
    )