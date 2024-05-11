from models.entity import Entity

class EnergyEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            energy=0,
            energy_limit=0,
            ts_previous_use=0,
        ):
        self.table_name: str = 'energy'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.energy: int = energy
        self.energy_limit: int = energy_limit
        self.ts_previous_use: int = ts_previous_use