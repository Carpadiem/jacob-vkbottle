from vkbottle import Keyboard, Text, KeyboardButtonColor, Callback
from emojies import emojies

goto_property_shop = Keyboard(one_time=False, inline=True)
goto_property_shop.add(Callback(label=f'{ emojies.shopping_bags } Магазин имущества', payload={ 'action_type': 'button', 'action': 'show_property_shop' }), color=KeyboardButtonColor.SECONDARY)
goto_property_shop = goto_property_shop.get_json()

property_shop = Keyboard(one_time=False, inline=True)
property_shop.add(Callback(label=f'{ emojies.phone } Телефоны', payload={ 'action_type': 'button', 'action': 'property_shop_category', 'category': 'phones' }), color=KeyboardButtonColor.SECONDARY)
property_shop.row()
property_shop.add(Callback(label=f'{ emojies.desktop } Компьютеры', payload={ 'action_type': 'button', 'action': 'property_shop_category', 'category': 'computers' }), color=KeyboardButtonColor.SECONDARY)
property_shop.row()
property_shop.add(Callback(label=f'{ emojies.television } Телевизоры', payload={ 'action_type': 'button', 'action': 'property_shop_category', 'category': 'tvs' }), color=KeyboardButtonColor.SECONDARY)
property_shop.row()
property_shop.add(Callback(label=f'{ emojies.cyclone } Стиралки', payload={ 'action_type': 'button', 'action': 'property_shop_category', 'category': 'washing_machines' }), color=KeyboardButtonColor.SECONDARY)
property_shop.row()
property_shop.add(Callback(label=f'{ emojies.mans_shoe } Тяги', payload={ 'action_type': 'button', 'action': 'property_shop_category', 'category': 'shoes' }), color=KeyboardButtonColor.SECONDARY)
property_shop.row()
property_shop.add(Text(label=f'{ emojies.key } Назад (Мое имущество)', payload={ 'action_type': 'button', 'action': 'show_my_property' }), color=KeyboardButtonColor.SECONDARY)
property_shop = property_shop.get_json()