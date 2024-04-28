# imports
from random import choices, randrange
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
# rules
from rules import PayloadContainsOrTextRule
from vkbottle.dispatch.rules.base import PayloadContainsRule
# database
from database.repository import Repository
from database.entities import PlayerEntity
from database.entities import CasesEntity
# emojies
from emojies import emojies
# templates
from templates import templates
# game data
from constants import game_cases
# tools
from tools import error_message
from utils.log import Log

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())

# handlers
@bl.message(text=['бизнесы', 'бизнес'])
async def business_shop(m: Message):
    pass