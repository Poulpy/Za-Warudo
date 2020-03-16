import csv
import sys
from user import User
from debate import Debate
from projection_room import ProjectionRoom
from debate import Debate
from event import Event
from team import Team
from peewee import SqliteDatabase
import logging as log

db = SqliteDatabase("db/app.db")
SEED_FILE = "db/seed.csv"
MODELS = (User, ProjectionRoom, Team, Debate, Event)

def seed():
    with open(SEED_FILE) as csv_file:
        log.info("Seeding the database")
        db.connect()

        db.create_tables([User, ProjectionRoom, Team, Debate, Event], safe = True)
        log.info("Tables created")

        User.create(name="admin", login="admin", password="admin")
        log.info("Administrator created")

        csv_reader = csv.reader(csv_file, delimiter=",")

        for row in csv_reader:
            User.create(name=row[0], login=row[1], password=row[2])

        db.close()

def drop():
    db.connect()
    db.drop_tables([User, ProjectionRoom, Team, Debate, Event], safe = True)
    log.info("Tables dropped")
    db.close()

def select():
    db.connect()
    for table in MODELS:
        for i in table.select():
            print(i)
    db.close()

if __name__ == "__main__":
    log.basicConfig(filename="log.txt", level=log.INFO)
    log.getLogger().addHandler(log.StreamHandler(sys.stdout))

    if len(sys.argv) > 0:
        if sys.argv[1] == "seed":
            seed()
        elif sys.argv[1] == "drop":
            drop()
        elif sys.argv[1] == "select":
            select()


