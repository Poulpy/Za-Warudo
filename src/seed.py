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
import os

db = SqliteDatabase("db/app.db")
SEED_FILES_DIR = "db/seed_files/"
USERS_SEED_FILE = "users.csv"
MODELS = (User, ProjectionRoom, Team, Debate, Event)


def get_class(kls):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def seed():
    '''
    First row : name of the class
    Second row : name of the fields to seed, in the right order
    Other rows : datas
    '''
    db.connect()
    tables = []
    datas = []
    seeds = []

    for root, dirs, files in os.walk(SEED_FILES_DIR):
        for seed_file in files:
            seeds = []
            with open(root + seed_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                datas = list(csv_reader)
                klass = (datas.pop(0))[0]
                fields = datas.pop(0)

                M = get_class(klass)
                tables.append(M)

                for data in datas:
                    seeds.append({fields[i]:data[i] for i in range(len(data))})

            log.info("Parsing done")
            print(seeds)

    log.info("Seeding done")
    print(tables)

    db.close()

    '''
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
        '''

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
    log.basicConfig(filename="log/seed.txt", level=log.INFO)
    log.getLogger().addHandler(log.StreamHandler(sys.stdout))

    if len(sys.argv) > 0:
        if sys.argv[1] == "seed":
            seed()
        elif sys.argv[1] == "drop":
            drop()
        elif sys.argv[1] == "select":
            select()


