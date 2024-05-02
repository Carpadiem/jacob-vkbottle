from . import start, z_unknown_command
from .general import help, profile, money, bank, cases, business, job, energy
from .games import cube, cup, casino
from .misc import picture, donate, report

labelers = [

    picture.bl,
    donate.bl,
    report.bl,

    casino.bl,
    cube.bl,
    cup.bl,

    start.bl,
    help.bl,
    profile.bl,
    money.bl,
    bank.bl,
    cases.bl,
    business.bl,
    job.bl,
    energy.bl,

    z_unknown_command.bl,
]