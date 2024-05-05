from typing import List
from vkbottle.dispatch.rules.base import BaseMessageMin, ABCRule, PayloadContainsRule

class PayloadContainsOrTextRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload: dict, text: str | List[str]):
        self.payload = payload
        self.text = text

    async def check(self, event: BaseMessageMin) -> bool:

        isPayloadContains = await PayloadContainsRule(self.payload).check(event)
        isText = False

        if type(self.text) == str:
            isText = self.text.lower() == event.text.lower()
        elif type(self.text) == list:
            isText = event.text.lower() in [x.lower() for x in self.text]

        return isPayloadContains or isText