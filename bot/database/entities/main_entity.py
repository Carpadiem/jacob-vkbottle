from models.entity import Entity

class MainEntity(Entity):
    def __init__(self):
        self.table_name: str = 'main'

        self.player_id: int = 0
        self.user_id: int = 0
        self.nickname: str = ''

    def set_values(self):
        pass