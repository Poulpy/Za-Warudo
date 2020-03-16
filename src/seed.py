from peewee import SqliteDatabase
from models import User, ProjectionRoom, Team, Debate, Event
"""
from models.User import User
from models.Event import Event
from models.Team import Team
from models.ProjectionRoom import ProjectionRoom
from models.Debate import Debate
"""

db = SqliteDatabase("db/app.db")
SEED_FILE = "db/seed.csv"

with open(SEED_FILE) as csv_file:
    db.connect()
    db.create_tables([User, ProjectionRoom, Team, Debate, Event])
    print("> Tables created")

    csv_reader = csv.reader(csv_file, delimiter=",")

    for row in csv_reader:
        User.create(name=row[0], login=row[1], password=row[2])

    db.close()

