# imports
# vkbottle
from vkbottle import TemplateElement, template_gen
from vkbottle import Keyboard, KeyboardButtonColor, Text
# game data
from constants import game_businesses

template_elements = []

for k, data in game_businesses.items():
    name = data['name']
    desc = data['desc'] + 't'
    price = data['price']
    earnings_per_hour = data['options']['earnings_per_hour']
    # template buttons
    keyboard = Keyboard()
    keyboard.add(Text(label='Приобрести', payload={ 'action_type': 'button', 'action': 'buy_business', 'business_id': k }), color=KeyboardButtonColor.SECONDARY)
    keyboard = keyboard.get_json()
    template_elements.append(TemplateElement(title=name, description=desc, buttons=keyboard))

template = template_gen(*template_elements)