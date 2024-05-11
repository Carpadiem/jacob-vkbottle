# imports
# vkbottle
from vkbottle.bot import BotLabeler, Message
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity
from database.repository import Repository
# emojies
from emojies import emojies
# tools
from tools.get_player_profile_text import get_player_profile_text
# constants
from constants import max_player_energy as MAX_PLAYER_ENERGY

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())


# handlers
@bl.message(PayloadContainsOrTextRule(payload={ 'action_type': 'button', 'action': 'show_profile' }, text='профиль'))
async def profile(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })

    player_profile_lines_text = await get_player_profile_text(player.player_id)

    text = f'''{ emojies.ledger } { player.nickname }, Ваш профиль:

    {player_profile_lines_text}
    '''.replace('    ', '')

    await m.answer(text)