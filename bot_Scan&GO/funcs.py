from data.DataBase.db import BotDB

db = BotDB('C:/Workplace/Новая папка/data/DataBase/botbd.db')

results = db.take_rec(9)

print(db.take_rec(9))
