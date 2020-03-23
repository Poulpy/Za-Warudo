import csv
import logging as log
import os
import sys

from peewee import SqliteDatabase
from playhouse.reflection import print_table_sql

from models.user import User
from models.category import Category
from models.debate import Debate
from models.event import Event
from models.events_category import EventsCategory
from models.projection_room import ProjectionRoom
from models.team import Team
from models.vacation import Vacation

db = SqliteDatabase("db/app.db")

# The files containing datas; these datas will be used to fill
# the database
SEED_FILES_DIR = "db/seed_files/"

# All the models/tables of the database
# TODO make it dynamic by putting the models in a package/module
MODELS = (User, ProjectionRoom, Team, Debate, Event, Category,
          EventsCategory, Vacation)


def get_class(kls):
    '''
    module, klass = kls.split('.')
    return getattr(__import__(module), klass)
    '''
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m

def seed():
    '''
    Fill the database with datas
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

    User.create(name="Admin", login="admin", password="admin", is_admin=True)

    for root, dirs, files in os.walk(SEED_FILES_DIR):
        # We look for each seed file, and then we parse the datas
        for seed_file in files:
            seeds = []

            with open(root + seed_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                datas = list(csv_reader)

                # We take out the table name and its fields
                klass = (datas.pop(0))[0]
                fields = datas.pop(0)

                # then we parse the datas
                for data in datas:
                    seeds.append({fields[i]:data[i] for i in range(len(data))})

            log.info("Seeding %s..." % (klass))
            Table = get_class('models.' + klass)
            Table.insert_many(seeds).execute()
            log.info("Seeding done for %s" % (klass))

    log.info("Seeding done")
    db.close()

def drop():
    '''
    Remove all tables
    '''
    db.connect()

    tables = list(MODELS)

    log.info("Dropping all tables")
    db.drop_tables(tables, safe = True)
    log.info("Tables dropped")

    db.close()

def desc():
    '''
    Gives a description of all tables: the fields and
    their types
    '''

    db.connect()

    for table in MODELS:
        print_table_sql(table)

    db.close()

def select():
    '''
    Show all datas stored in the database
    TODO accept argument for specific table
    '''

    db.connect()

    for table in MODELS:
        for i in table.select().dicts():
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
        elif sys.argv[1] == "desc":
            desc()

