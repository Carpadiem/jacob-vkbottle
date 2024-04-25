from vkbottle import Bot
from routes import labelers
import config
from middlewares import each_message

bot = Bot(config.VK_TOKEN)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

if __name__ == '__main__':
    try:
        bot.labeler.message_view.register_middleware(each_message)
        bot.run_forever()
    except: pass
