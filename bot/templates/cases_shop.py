# imports
# vkbottle
from vkbottle import TemplateElement, template_gen
from vkbottle import Keyboard, KeyboardButtonColor, Text
# game data
from constants import game_cases

def func_template(counts: list):
    template_elements = []
    for k, case_data in game_cases.items():
        # case data
        name = case_data['name']
        desc = case_data['desc']
        # template buttons
        keyboard = Keyboard(one_time=False, inline=False)
        keyboard.add(Text(label='Купить', payload={ 'action_type': 'button', 'action': 'buy_case', 'case_id': k }), color=KeyboardButtonColor.SECONDARY)
        keyboard.add(Text(label=f'Открыть ({counts[k-1]} шт.)', payload={ 'action_type': 'button', 'action': 'open_case', 'case_id': k }), color=KeyboardButtonColor.PRIMARY)
        keyboard.add(Text(label='Информация', payload={ 'action_type': 'button', 'action': 'info_case', 'case_id': k }), color=KeyboardButtonColor.SECONDARY)
        keyboard = keyboard.get_json()
        # add templateElement to array
        template_elements.append(TemplateElement(title=name, description=desc, buttons=keyboard))

    return template_gen(*template_elements)
