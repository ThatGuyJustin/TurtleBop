import os
import yaml

from peewee import Proxy, OP, Model
from peewee import Expression
from playhouse.postgres_ext import PostgresqlExtDatabase

with open("config.yaml", 'r') as stream:
    databaseconfig = yaml.safe_load(stream)['postgres']

REGISTERED_MODELS = []

# Create a database proxy we can setup post-init
database = Proxy()

OP['IRGX'] = 'irgx'

PostgresqlExtDatabase.register_ops({OP.IRGX: '~*'})

class BaseModel(Model):
    class Meta:
        database = database

    @staticmethod
    def register(cls):
        REGISTERED_MODELS.append(cls)
        return cls

def init_db():
    database.initialize(PostgresqlExtDatabase(
        databaseconfig['database'],
        host=databaseconfig['host'],
        user=databaseconfig['username'],
        password=databaseconfig['password'],
        port=int(databaseconfig['port']),
        autorollback=True))

    for model in REGISTERED_MODELS:
        model.create_table(True)

        if hasattr(model, 'SQL'):
            database.execute_sql(model.SQL)