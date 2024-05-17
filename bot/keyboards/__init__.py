from .misc import misc
from .games import games, cube, cup, casino
from .general import (
    general,
    jobs,
    bank,
    business,
    donate,
    property,
)
from .vehicle import (
    autosalone_pages_inline,
    garage_vehicles_inline,
    back_to_garage_inline,
    motortransport_start,
)
from . import (
    start,
)

keyboards = {
    'start': start.keyboard,
    'general': general.keyboard,
    
    'bank': bank.keyboard,
    'bank_cancel': bank.keyboard_cancel,

    'business': business.keyboard,
    'my_business': business.keyboard_my_business,

    'jobs': jobs.keyboard,
    
    'games': games.keyboard,
    'game_cube': cube.keyboard,
    'game_cup': cup.keyboard,
    'game_casino': casino.keyboard,

    'misc': misc.keyboard,

    'donate': donate.keyboard,

    'goto_property_shop': property.goto_property_shop,
    'property_shop': property.property_shop,

    'motor_transport_start': motortransport_start.keyboard,
    'autosalone_pages_inline': autosalone_pages_inline.func_keyboard,
    
    'player_garage_inline': garage_vehicles_inline.func_keyboard,
    'back_to_player_garage_inline': back_to_garage_inline.keyboard,
}