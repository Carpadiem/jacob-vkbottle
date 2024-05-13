from models.entity import Entity

class VehiclesEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            vehicles=''
        ):
        self.table_name: str = 'vehicles'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.vehicles: str = vehicles