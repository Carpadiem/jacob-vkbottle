# imports
# datetime
from datetime import datetime
# vkbottle
from vkbottle.bot import Message
from vkbottle import BaseMiddleware
# database
from database.repository import Repository
from database.entities import PlayerEntity, BankEntity, CasesEntity, BusinessEntity, EnergyEntity, PropertyEntity
from utils.log import Log

# init repo
playerRepo = Repository(entity=PlayerEntity())


class ACSMessage(BaseMiddleware[Message]):
    async def post(self):
        pass