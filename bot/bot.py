from vkbottle import Bot
from routes import labelers
import config

bot = Bot(config.VK_TOKEN)

for custom_labeler in labelers:
    bot.labeler.load(custom_labeler)

if __name__ == '__main__':
    try: bot.run_forever()
    except: pass
