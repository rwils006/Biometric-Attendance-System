import sqlite3

class Database:
    
    def __init__(self, db):
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (sid text, first text, last text)")
        self.conn.commit()
    
    def fetch(self):
        
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, sid, first, last):
        
        self.cur.execute("INSERT INTO students VALUES (NULL, ?, ?, ?)", (sid, first, last))
        self.conn.commit()
        
    def remove(self, id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()
    
    def update(self, id, sid, first, last):
        
        self.cur.execute("UPDATE students SET sid = ?, first = ?, last = ? WHERE id = ?", (sid, first, last))
        self.conn.commit()
        
    def __del__(self):
        
        self.conn.close()
        
db = Database('students.db')

for row in db.fetch():
    print(row)