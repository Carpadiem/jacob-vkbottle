from models.entity import Entity

class VehiclesEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            vehicles='',
            garage_slots_limit=0,
        ):
        self.table_name: str = 'vehicles'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.vehicles: str = vehicles
        self.garage_slots_limit: int = garage_slots_limit