import csv
from user import User
from debate import Debate
from projection_room import ProjectionRoom
from debate import Debate
from event import Event
from team import Team
from peewee import SqliteDatabase

db = SqliteDatabase("db/app.db")
SEED_FILE = "db/seed.csv"

with open(SEED_FILE) as csv_file:
    db.connect()
    db.create_tables([User, ProjectionRoom, Team, Debate, Event], safe = True)
    print("> Tables created")

    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:
        User.create(name=row[0], login=row[1], password=row[2])

    db.close()

