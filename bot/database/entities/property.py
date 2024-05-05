from models.entity import Entity

class PropertyEntity(Entity):
    def __init__(
            self, 
            player_id=0,
            user_id=0,
            phone_id=0,
            computer_id=0,
            tv_id=0,
            washing_machine_id=0,
            shoes_id=0,
        ):
        self.table_name: str = 'property'
        self.player_id: int = player_id
        self.user_id: int = user_id
        self.phone_id: int = phone_id        
        self.computer_id: int = computer_id
        self.tv_id: int = tv_id
        self.washing_machine_id: int = washing_machine_id
        self.shoes_id: int = shoes_id