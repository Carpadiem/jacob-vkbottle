from vkbottle.bot import Message
from config_states import my_state_dispenser

async def clear_current_state(m: Message):
    current_state = await my_state_dispenser.get(m.peer_id)
    if current_state != None: await my_state_dispenser.delete(m.peer_id)