# imports
from random import randrange
# vkbottle
from vkbottle.bot import BotLabeler, Message
from vkbottle.dispatch.rules.base import PayloadContainsRule
# rules
from rules import PayloadContainsOrTextRule
# database
from database.entities import PlayerEntity, EnergyEntity
from database.repository import Repository
# emojies
from emojies import emojies
# keyboards
from keyboards import keyboards
# constants
from constants import game_jobs
from constants import job_adding_experience as JOB_ADDING_EXPERIENCE
from constants import max_player_energy as MAX_PLAYER_ENERGY
from constants import energy_recovery_time_in_minutes as ENERGY_RECOVERY_TIME_IN_MINUTES
# tools
from tools import get_energy, use_energy, error_message

# create labeler
bl = BotLabeler()
bl.vbml_ignore_case = True

# repos
playerRepo = Repository(entity=PlayerEntity())
energyRepo = Repository(entity=EnergyEntity())

# handlers
@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'show_jobs' }))
async def show_job(m: Message):
    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    # answer
    text = f'''{ emojies.desktop } { player.nickname }, Меню работ в игре:'''
    await m.answer(message=text, keyboard=keyboards['jobs'])


@bl.message(PayloadContainsRule({ 'action_type': 'button', 'action': 'job_work' }))
async def job_work(m: Message):
    
    payload = m.get_payload_json()
    job_id = payload['job_id']

    # entities
    player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': m.from_id })
    energy: EnergyEntity = await energyRepo.find_one_by({ 'user_id': m.from_id })

    # check is player have any energy
    player_energy = await get_energy(m.from_id)
    if player_energy < 1:
        text = f'''{ emojies.sparkles } { player.nickname }, У вас 0 энергии

        { emojies.tip } Подождите {ENERGY_RECOVERY_TIME_IN_MINUTES} мин., чтобы восстановить 1 ед. энергии
        '''.replace('    ', '')
        await error_message(m, text)
        return
    
    # check is player have experience for work
    job_requirements_experience = game_jobs[job_id]['requirements']['experience']
    if player.experience < job_requirements_experience:
        text = f'''{ emojies.sparkles } { player.nickname }, Вам не хватает опыта, чтобы работать на этой работе ({job_requirements_experience:,} { emojies.trophy })

        { emojies.tip } Сейчас у вас {player.experience:,} { emojies.trophy }
        { emojies.tip } Работайте, зарабатывайте опыт и продвигайте свою карьеру
        '''.replace('    ', '')
        await error_message(m, text)
        return
    
    # calculate earnings
    job_earnings_money = game_jobs[job_id]['earnings_money']
    e_min = job_earnings_money['min']
    e_max = job_earnings_money['max']
    e_step = job_earnings_money['step']
    earnings = randrange(e_min, e_max, e_step)

    # update money
    await playerRepo.update({ 'user_id': m.from_id }, { 'money': player.money + earnings })
    # update experience
    await playerRepo.update({ 'user_id': m.from_id }, { 'experience': player.experience + JOB_ADDING_EXPERIENCE })
    # update energy
    await use_energy(m.from_id)

    # answer
    text = f'''{ emojies.desktop } { player.nickname }, Успешный рабочий день!

    + ${earnings:,} { emojies.dollar_banknote }
    + {JOB_ADDING_EXPERIENCE:,} { emojies.trophy }
    - 1 { emojies.high_voltage }
    '''.replace('    ', '')
    await m.answer(text)

    



