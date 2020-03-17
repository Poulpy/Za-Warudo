import csv
import sys
import logging as log
import os
from peewee import SqliteDatabase
from user import User
from debate import Debate
from projection_room import ProjectionRoom
from debate import Debate
from event import Event
from team import Team
from category import Category
from seats_category import SeatsCategory
from vacation import Vacation

db = SqliteDatabase("db/app.db")
SEED_FILES_DIR = "db/seed_files/"
USERS_SEED_FILE = "users.csv"
MODELS = (User, ProjectionRoom, Team, Debate, Event, Category,
          SeatsCategory, Vacation)


def get_class(kls):
    module, klass = kls.split('.')
    return getattr(__import__(module), klass)
    '''
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m
    '''

def seed():
    '''
    First row : name of the class
    Second row : name of the fields to seed, in the right order
    Other rows : datas
    '''
    db.connect()
    datas = []
    klass = ""
    log.info("Creating the tables...")
    db.create_tables(list(MODELS))
    log.info("Tables created")
    log.info("Seeding...")

    for root, dirs, files in os.walk(SEED_FILES_DIR):
        for seed_file in files:
            seeds = []

            with open(root + seed_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                datas = list(csv_reader)

                klass = (datas.pop(0))[0]
                fields = datas.pop(0)

                for data in datas:
                    seeds.append({fields[i]:data[i] for i in range(len(data))})

            log.info("Seeding %s..." % (klass))
            Table = get_class(klass)
            Table.insert_many(seeds).execute()

            log.info("Parsing done for %s" % (klass))

    log.info("Seeding done")
    db.close()

def drop():
    db.connect()

    tables = list(MODELS)

    log.info("Dropping all tables")
    db.drop_tables(tables, safe = True)
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

