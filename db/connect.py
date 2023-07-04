import sqlite3 as sq
global base,cur
async def connection():

    base = sq.connect('main.db')
    cur = base.cursor()
    # if base:
    #     print("DATABASE CONNECTED OK!")
    base.execute(f"CREATE TABLE IF NOT EXISTS Users"
                 f"("
                 f"id INTEGER,"
                 f"datatime REAL,"
                 f"callback INTEGER,"
                 f"link TEXT,"
                 f"ban INTEGER,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS Scripts"
                 f"("
                 f"id INTEGER,"
                 f"name TEXT,"
                 f"description TEXT,"
                 f"price REAL,"
                 f"img TEXT,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS UserState"
                 f"("
                 f"id INTEGER,"
                 f"callback INTEGER,"
                 f"state INTEGER,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS Projects"
                 f"("
                 f"id INTEGER,"
                 f"name TEXT,"
                 f"img TEXT,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS UserStateProjects"
                 f"("
                 f"id INTEGER,"
                 f"callback INTEGER,"
                 f"state INTEGER,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS Statisticks"
                 f"("
                 f"id INTEGER,"
                 f"start INTEGER,"
                 f"info INTEGER,"
                 f"channels INTEGER,"
                 f"button_about INTEGER,"
                 f"button_ourProjects INTEGER,"
                 f"button_consultate INTEGER,"
                 f"button_contacts INTEGER,"
                 f"button_scripts INTEGER,"
                 f"button_jokes INTEGER,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS Jokes"
                 f"("
                 f"id INTEGER,"
                 f"name TEXT,"
                 f"joke TEXT,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    base.execute(f"CREATE TABLE IF NOT EXISTS UserStateJokes"
                 f"("
                 f"id INTEGER,"
                 f"callback INTEGER,"
                 f"state INTEGER,"
                 f"PRIMARY KEY('id' AUTOINCREMENT))")
    base.commit()
    return base,cur

# def my_base():
#     return base
# def my_cur():
#     return cur

