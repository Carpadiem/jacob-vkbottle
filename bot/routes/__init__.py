from . import start, z_unknown_command
from .general import help, profile, money, bank, cases, business, job, energy, property
from .games import cube, cup, casino
from .misc import picture, donate, report
from .privilege.player import nickname
from .admin import admin_manager

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
    # privilege
    nickname.bl,
    # admin manager
    admin_manager.bl,
    # unknown command
    z_unknown_command.bl,
]