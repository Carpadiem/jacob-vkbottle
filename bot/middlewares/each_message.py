# imports
# datetime
from datetime import datetime
# vkbottle
from vkbottle.bot import Message
from vkbottle import BaseMiddleware
# database
from database.repository import Repository
from database.entities import PlayerEntity, BankEntity, CasesEntity, BusinessEntity, EnergyEntity, PropertyEntity
from utils.log import Log

# init repo
playerRepo = Repository(entity=PlayerEntity())
bankRepo = Repository(entity=BankEntity())
casesRepo = Repository(entity=CasesEntity())
businessRepo = Repository(entity=BusinessEntity())
energyRepo = Repository(entity=EnergyEntity())
propertyRepo = Repository(entity=PropertyEntity())


class EachMessage(BaseMiddleware[Message]):
    async def pre(self):
        sender = await self.event.get_user()
        sender_id = sender.id
        sender_first_name = sender.first_name

        player_id = 0

        # Try find user in db.
        # Generate player_id if not exist.
        player: PlayerEntity = await playerRepo.find_one_by({ 'user_id': sender_id })
        if player == None:
            player_id = await playerRepo.count() + 1
        else:
            player_id = player.player_id

        # now timestamp for ts_registration column in db
        ts_now = datetime.now().timestamp()
        ts_now = str(ts_now)
        ts_now = int(ts_now.split('.')[0])

        # entity_like = {
        #     'player_id': player_id,
        #     'user_id': sender_id,
        #     'nickname': sender_first_name
        # }
        # entity: PlayEntity = playerRepo.create(entity_like)
        # mainRepo.save(entity)

        # init player-player in table
        playerEntity: PlayerEntity = PlayerEntity(
            player_id=player_id,
            user_id=sender_id,
            nickname=sender_first_name,
            money=0,
            ts_registration=ts_now,
        )
        try: await playerRepo.save(playerEntity)
        except Exception as e: Log(f'[exception][each_middleware / save player entity]: {e}')
        
        # init player-bank in table
        bankEntity: BankEntity = BankEntity(
            player_id=player_id,
            user_id=sender_id,
            score=0,
            transfers_left=20,
            transfers_limit=20,
            ts_previous_transfer=ts_now,
        )
        try: await bankRepo.save(bankEntity)
        except Exception as e: Log(f'[exception][each_middleware / save bank entity]: {e}')

        # init player-cases in table
        casesEntity: CasesEntity = CasesEntity(
            player_id=player_id,
            user_id=sender_id,
            count_1=0,
            count_2=0,
            count_3=0,
            count_4=0,
        )
        try: await casesRepo.save(casesEntity)
        except Exception as e: Log(f'[exception][each_middleware / save cases entity]: {e}')

        # init bank
        businessEntity: BusinessEntity = BusinessEntity(
            player_id=player_id,
            user_id=sender_id,
            business_id=0,
            ts_previous_profit=ts_now,
        )
        try: await businessRepo.save(businessEntity)
        except Exception as e: Log(f'[exception][each_middleware / save business entity]: {e}')

        # init energy
        energyEntity: EnergyEntity = EnergyEntity(
            player_id=player_id,
            user_id=sender_id,
            energy=20,
            ts_previous_use=ts_now,
        )
        try: await energyRepo.save(energyEntity)
        except Exception as e: Log(f'[exception][each_middleware / save energy entity]: {e}')

        # init property
        propertyEntity: PropertyEntity = PropertyEntity(
            player_id=player_id,
            user_id=sender_id,
            phone_id=0,
            computer_id=0,
            tv_id=0,
            washing_machine_id=0,
            shoes_id=0,
        )
        try: await propertyRepo.save(propertyEntity)
        except Exception as e: Log(f'[exception][each_middleware / save property entity]: {e}')