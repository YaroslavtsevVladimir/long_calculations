import sqlite3


connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS results (
        id TEXT PRIMARY KEY,
        result INTEGER NOT NULL
    );
    '''
)

connection.commit()
connection.close()
