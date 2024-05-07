# imports
from typing import List
# vkbottle
from vkbottle.dispatch.rules.base import BaseMessageMin, ABCRule
# database
from database.repository import Repository
from database.entities import PlayerEntity

# init repos
playerRepo = Repository(entity=PlayerEntity())

class RoleRule(ABCRule[BaseMessageMin]):
    def __init__(self, roles: str | List[str]):
        if isinstance(roles, str): self.roles = [roles]
        self.roles = roles

    async def check(self, event: BaseMessageMin) -> bool:
        # entities
        player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': event.from_id })
        if player.role in self.roles:
            return True
        else:
            return False