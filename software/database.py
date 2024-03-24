import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                gameText TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def addText(self, game_text):
        self.cursor.execute('''
            INSERT INTO games (gameText) VALUES (?)
        ''', (game_text,))
        self.conn.commit()

    def getAllTexts(self):
        self.cursor.execute('''
            SELECT * FROM games
        ''')
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()