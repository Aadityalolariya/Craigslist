from peewee import Model, IntegerField, TextField, FloatField, SqliteDatabase

db = SqliteDatabase('./Craigslist/data.db')

class Craigslist(Model):
    id = TextField(primary_key=True)
    latitude = FloatField()
    longitude = FloatField()
    userId = TextField()
    description = TextField(null=True)
    price = IntegerField()
    status = TextField()

    class Meta:
        database = db
        db_table = "Craigslist"
