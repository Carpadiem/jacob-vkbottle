from typing import Union, List
from vkbottle.dispatch.rules.base import BaseMessageMin, ABCRule
from tools.isSubset import isSubset

class PayloadContainsOrNotRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload: dict):
        self.payload = payload

    async def check(self, event: BaseMessageMin) -> bool:
        message_payload = event.get_payload_json()
        if message_payload == None:
            return True
        if isSubset(list(message_payload.items()), list(self.payload.items())):
            return True
        else:
            return False