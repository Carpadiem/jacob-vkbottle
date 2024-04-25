from mysql.connector.aio import connect as mysql_connect
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

    async def connect(self):
        try:
            self.connection = await mysql_connect(**connection_config)
            self.cursor = await self.connection.cursor(buffered=True, dictionary=True)
        except Exception as e:
            Log(f'[exception][repository.py / def connect]: {e}')

    async def find_one_by(self, where: dict):
        '''Example `where` argument: `{ 'user_id': 230990098 }`'''
        try:
            # split where
            where_key = list(where.keys())[0]
            where_value = list(where.values())[0]
            # open connection & make query
            await self.connect()
            query = f'SELECT * FROM {self.entity.table_name} WHERE {where_key}="{where_value}"'
            await self.cursor.execute(query)
            row: dict = await self.cursor.fetchone()
            if row == None:
                return None
            # change python-variable of object by string data
            for k, v in row.items():
                setattr(self.entity, k, v)
            # save & close connection
            await self.close()
            return self.entity
        except Exception as e:
            Log(f'[exception][repository.py / def find_one_by]: {e}')
    
    async def create(self, entity_like: dict) -> Entity:
        try:
            new_entity: type[self.entity] = self.entity
            for k, v in entity_like.items():
                setattr(new_entity, k, v)
            return new_entity
        except Exception as e:
            Log(f'[exception][repository.py / def create]: {e}')

    async def save(self, entity: Entity):
        try:
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
            # open connection, make query, close connection
            await self.connect()
            query = f'INSERT IGNORE INTO {table_name} ({", ".join(keys)}) VALUES ({", ".join([str(x) for x in values])})'
            await self.cursor.execute(query)
            await self.close()
        except Exception as e:
            Log(f'[exception][repository.py / def save]: {e}')

    async def update(self, where: dict, field: dict):
        try:
            table_name = self.entity.table_name
            # split where, field
            where_key = list(where.keys())[0]
            where_value = list(where.values())[0]
            field_key = list(field.keys())[0]
            field_value = list(field.values())[0]
            # open, make query, close
            await self.connect()
            query = f'UPDATE {table_name} SET {field_key}="{field_value}" WHERE {where_key}="{where_value}"'
            await self.cursor.execute(query)
            await self.close()
        except Exception as e:
            Log(f'[exception][repository.py / def update]: {e}')

    
    async def count(self):
        try:
            await self.connect()
            query = f'SELECT * FROM {self.entity.table_name}'
            await self.cursor.execute(query)
            row = await self.cursor.fetchall()
            await self.close()
            return len(row)
        except Exception as e:
            Log(f'[exception][repository.py / def count]: {e}')
    
    async def close(self):
        try:
            await self.connection.commit()
            await self.cursor.close()
            await self.connection.close()
        except Exception as e:
            Log(f'[exception][repository.py / def close]: {e}')
        
