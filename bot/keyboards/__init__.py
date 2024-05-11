from . import (
    jobs,
    start,
    general,
    bank,
    business,
    games,
    misc,
    donate,
    property,
    motor_transport_start,
    autosalone_pages_inline
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
    'game_cube': games.keyboard_game_cube,
    'game_cup': games.keyboard_game_cup,
    'game_casino': games.keyboard_game_casino,

    'misc': misc.keyboard,

    'donate': donate.keyboard,

    'goto_property_shop': property.goto_property_shop,
    'property_shop': property.property_shop,

    'motor_transport_start': motor_transport_start.keyboard,
    'autosalone_pages_inline': autosalone_pages_inline.func,
}