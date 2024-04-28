from models.entity import Entity

class CasesEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            count_1=0,
            count_2=0,
            count_3=0,
            count_4=0,
        ):
        self.table_name: str = 'cases'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.count_1: int = count_1
        self.count_2: int = count_2
        self.count_3: int = count_3
        self.count_4: int = count_4