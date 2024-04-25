import mysql.connector
from models.entity import Entity

connection_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'jacob_db',
}

class Repository:
    def __init__(self, entity: Entity):
        self.entity = entity

    def connect(self):
        self.connection = mysql.connector.connect(**connection_config)
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)

    def find_one_by(self, where: dict):
        '''
        Example `where` argument: `{ 'user_id': 230990098 }`
        '''
        # open connection
        self.connect()
        # split where
        where_key = list(where.keys())[0]
        where_value = list(where.values())[0]
        # make query
        query = f'SELECT * FROM {self.entity.table_name} WHERE {where_key}="{where_value}"'
        self.cursor.execute(query)
        row: dict = self.cursor.fetchone()
        # change python-variable of object by string data
        for k, v in row.items():
            setattr(self.entity, k, v)
        # save & close connection
        self.close()
        return self.entity
    
    def close(self):
        self.connection.commit()
        self.connection.close()
        
