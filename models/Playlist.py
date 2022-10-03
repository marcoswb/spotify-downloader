from peewee import *

database_file = SqliteDatabase('memory.db')

class Playlist(Model):
    link = CharField()

    class Meta:
        database = database_file