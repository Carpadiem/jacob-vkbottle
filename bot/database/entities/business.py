from models.entity import Entity

class BusinessEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            business_id=0,
            ts_previous_profit=0,
        ):
        self.table_name: str = 'business'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.business_id: int = business_id
        self.ts_previous_profit: int = ts_previous_profit