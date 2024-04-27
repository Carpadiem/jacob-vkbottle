from vkbottle import Bot
from routes import labelers
import config
from middlewares import each_message

from config_states import my_state_dispenser
bot = Bot(config.VK_TOKEN, state_dispenser=my_state_dispenser)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)


if __name__ == '__main__':
    try:
        bot.labeler.message_view.register_middleware(each_message)
        bot.run_forever()
    except: pass