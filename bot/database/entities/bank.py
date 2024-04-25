from models.entity import Entity

class BankEntity(Entity):
    def __init__(self):
        # table name
        self.table_name: str = 'bank'
        
        # columns
        self.player_id: int = 0
        self.user_id: int = 0
        self.score: int = 0
        self.transfers_left: int = 0
        self.transfers_limit: int = 0
        self.previous_transfer_timestamp: int = 0