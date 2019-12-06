import sqlite3

class Database:
    
    def __init__(self, db):
        
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY, sid text, first text, last text, present text, uid integer)")
        self.conn.commit()
    
    def fetch(self):
        
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        return rows
    
    def insert(self, sid, first, last):
        
        self.cur.execute("INSERT INTO students VALUES (NULL, ?, ?, ?, ?, ?)",(sid, first, last, "A", 0))
        self.conn.commit()
        
    def remove(self, id):
        self.cur.execute("DELETE FROM students WHERE id=?", (id,))
        self.conn.commit()
    
    def update(self, id, sid, first, last):
        
        self.cur.execute("UPDATE students SET sid = ?, first = ?, last = ? WHERE id = ?", (sid, first, last))
        self.conn.commit()
        
    def registerUID(self, id, uid):
        
        self.cur.execute("UPDATE students SET uid = ? WHERE id = ?", (uid, id))
        
    def changeToPresent(self, id):
        
        self.cur.execute("UPDATE students SET present = ? WHERE id = ?", ("P", id))
        self.conn.commit()
    
    def resetToAbsent(self):
        
        self.cur.execute("UPDATE students SET present = ?", ("A"))
        self.conn.commit()
    def fetch_SID_from_UID(self, uid):
        
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        
        for row in rows:
            
            if row[5] == uid:
                
                return row[1]
        return 0
        
    def fetchID(self, sid):
        
        self.cur.execute("SELECT * FROM students")
        rows = self.cur.fetchall()
        
        for row in rows:
            
            if row[1] == sid:
                
                return row[0]
        return 0
                
            
        
        
    def __del__(self):
        
        self.conn.close()
        
db = Database('students.db')

#db.changeToPresent(2)

for row in db.fetch():
    print(row)


