from peewee import *

database_file = SqliteDatabase('memory.db')

class Track(Model):
    playlist_id = IntegerField()
    name = CharField()
    link = CharField()

    class Meta:
        database = database_file