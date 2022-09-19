from peewee import *

database_file = SqliteDatabase('memory.db')

def create_tables():
    import peewee    
    models = peewee.Model.__subclasses__()
    database_file.create_tables(models)