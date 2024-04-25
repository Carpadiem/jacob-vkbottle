from typing import Union, List
from vkbottle.dispatch.rules.base import BaseMessageMin, ABCRule, PayloadContainsRule
from tools.isSubset import isSubset

class PayloadContainsOrTextRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload: dict, text: str):
        self.payload = payload
        self.text = text

    async def check(self, event: BaseMessageMin) -> bool:
        return await PayloadContainsRule(self.payload).check(event) or event.text == self.text