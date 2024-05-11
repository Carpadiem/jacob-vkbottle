from . import start, z_unknown_command
from .general import help, profile, money, bank, cases, business, job, energy, property
from .games import cube, cup, casino
from .misc import picture, donate, report

from .admin.routes.player import (
    role as acs_role,
    nickname as acs_nickname,
    money as acs_money,
    experience as acs_experience,
)
from .admin.routes.bank import (
    score_limit as acs_score_limit,
    score as acs_score,
    transfers as acs_transfers,
    transfers_limit as acs_transfers_limit
)
from .admin.routes.energy import (
    energy as acs_energy,
    energy_limit as acs_energy_limit,
)

labelers = [
    # start
    start.bl,
    # misc
    picture.bl,
    donate.bl,
    report.bl,
    # games
    casino.bl,
    cube.bl,
    cup.bl,
    # general
    help.bl,
    profile.bl,
    money.bl,
    bank.bl,
    cases.bl,
    business.bl,
    job.bl,
    energy.bl,
    property.bl,
    
    # admin routes
    # player
    acs_role.bl,
    acs_nickname.bl,
    acs_money.bl,
    acs_experience.bl,
    # bank
    acs_score_limit.bl,
    acs_score.bl,
    acs_transfers.bl,
    acs_transfers_limit.bl,
    # energy
    acs_energy.bl,
    acs_energy_limit.bl,
    
    # unknown command
    z_unknown_command.bl,
]