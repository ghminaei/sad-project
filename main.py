import database
from UserInterface import *

database.db = database.database("data.json")

commandHandler()

database.db.store("data.json")