from models.entity import Entity

class BankEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            score=0,
            transfers_left=0,
            transfers_limit=0,
            ts_previous_transfer=0,
        ):
        self.table_name: str = 'bank'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.score: int = score
        self.transfers_left: int = transfers_left
        self.transfers_limit: int = transfers_limit
        self.ts_previous_transfer: int = ts_previous_transfer