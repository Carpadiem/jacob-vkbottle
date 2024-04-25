from models.entity import Entity

class MainEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            nickname='',
            money=0,
            role='player',
            experience=0,
            special_currency=0,
            ts_registration=0,
        ):
        self.table_name: str = 'main'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.nickname: str = nickname
        self.money: int = money
        self.role: str = role
        self.experience: int = experience
        self.special_currency: int = special_currency
        self.ts_registration: int = ts_registration

    def set_values(self):
        pass