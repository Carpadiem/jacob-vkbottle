import mysql.connector
from models.entity import Entity
from tools.log import Log

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
        if row == None:
            return None
        # change python-variable of object by string data
        for k, v in row.items():
            setattr(self.entity, k, v)
        # save & close connection
        self.close()
        return self.entity
    
    def create(self, entity_like: dict) -> Entity:
        try:
            new_entity: type[self.entity] = self.entity
            for k, v in entity_like.items():
                setattr(new_entity, k, v)
            return new_entity
        except Exception as e:
            Log(f'[exception][repository.py / def create]: {e}')

    def save(self, entity: Entity):
        # reserve table_name        
        table_name = entity.table_name
        delattr(entity, 'table_name')
        # get attribtues and values as Columns and col-values
        keys = list(entity.__dict__.keys())
        values = list(entity.__dict__.values())
        # quoting values
        quoted_values: list = []
        for v in values:
            if type(v) == str:
                v = f'"{v}"'
            quoted_values.append(v)
        values = quoted_values
        # make query
        self.connect()
        query = f'INSERT IGNORE INTO {table_name} ({", ".join(keys)}) VALUES ({", ".join([str(x) for x in values])})'
        self.cursor.execute(query)
        self.close()

    
    def count(self):
        self.connect()
        query = f'SELECT * FROM {self.entity.table_name}'
        self.cursor.execute(query)
        row = self.cursor.fetchall()
        self.close()
        return len(row)
    
    def close(self):
        self.connection.commit()
        self.connection.close()
        
