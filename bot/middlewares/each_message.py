# imports
# datetime
from datetime import datetime
# vkbottle
from vkbottle.bot import Message
from vkbottle import BaseMiddleware
# database
from database.repository import Repository
from database.entities import MainEntity
from tools.log import Log

# init repo
mainRepo = Repository(entity=MainEntity())

class EachMessage(BaseMiddleware[Message]):
    async def pre(self):
        sender = await self.event.get_user()
        sender_id = sender.id
        sender_first_name = sender.first_name

        # try find user in db
        user = await mainRepo.find_one_by({ 'user_id': sender_id })
        if user == None:
            # generate player_id
            player_id = await mainRepo.count() + 1
            # now timestamp for ts_registration column in db
            ts_now = datetime.now().timestamp()
            ts_now = str(ts_now)
            ts_now = int(ts_now.split('.')[0])
            try:
                # entity_like = {
                #     'player_id': player_id,
                #     'user_id': sender_id,
                #     'nickname': sender_first_name
                # }
                # entity: MainEntity = mainRepo.create(entity_like)
                # mainRepo.save(entity)

                entity: MainEntity = MainEntity(
                    player_id=player_id,
                    user_id=sender_id,
                    nickname=sender_first_name,
                    money=0,
                    ts_registration=ts_now,
                )
                await mainRepo.save(entity)

            except Exception as e:
                Log(f'[exception][middlewares / class each_middleware]: {e}')