from SimpleDBUsingSqlite3 import SimpleDBUsingSqlite3
from config import *
name = '《剑来》'
dbClass = SimpleDBUsingSqlite3
columns = ['link_address']
db = dbClass(DATA_ABS_PATH + '/NovelUpdate_data', name, columns)
before =db.get_all()
print(len(before))
db.delete([before[len(before)-1][0]])
after =db.get_all()
print(len(after))