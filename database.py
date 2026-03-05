import sqlite3
from datetime import datetime

class PredictionHistory:
    def __init__(self, db_path="history.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_text TEXT NOT NULL,
                prediction TEXT NOT NULL,
                score REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_prediction(self, text, prediction, score):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO predictions (email_text, prediction, score, timestamp) VALUES (?, ?, ?, ?)",
                       (text, prediction, score, timestamp))
        conn.commit()
        conn.close()

    def get_all_predictions(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT prediction, COUNT(*) FROM predictions GROUP BY prediction")
        stats = dict(cursor.fetchall())
        conn.close()
        return {"Safe": stats.get("Safe", 0), "Phishing": stats.get("Phishing", 0)}

    def get_daily_trends(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DATE(timestamp), COUNT(*) 
            FROM predictions 
            WHERE prediction = 'Phishing' 
            GROUP BY DATE(timestamp) 
            ORDER BY DATE(timestamp) ASC 
            LIMIT 7
        """)
        trends = cursor.fetchall()
        conn.close()
        return trends

    def clear_history(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM predictions")
        
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='predictions'")
        
        conn.commit()
        conn.close()
