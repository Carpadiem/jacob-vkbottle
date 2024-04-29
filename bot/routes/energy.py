# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity, EnergyEntity
from database.repository import Repository
# emojies
from emojies import emojies
# const
from constants import max_player_energy as MAX_PLAYER_ENERGY
# tools
from tools import get_energy


# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())

# handlers
@bl.message(text=['энергия'])
async def energy(m: Message):
    # entites
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # ...
    player_energy = await get_energy(m.from_id)
    if player_energy > MAX_PLAYER_ENERGY:
        player_energy = MAX_PLAYER_ENERGY
    # answer
    text = f'{ emojies.high_voltage } { player.nickname }, У вас {player_energy:,} энергии'
    await m.answer(text)