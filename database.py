
import sqlite3
from datetime import datetime

class PredictionHistory:
    def __init__(self, db_path="C:/Users/Pranay/OneDrive/Desktop/Projects/FishyGuard/history.db"):
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
        cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows

if __name__ == '__main__':
    # for testing
    db = PredictionHistory()
    db.add_prediction("Test email", "Phishing", 0.99)
    db.add_prediction("Another test", "Safe", 0.95)
    
    print("All predictions:")
    for row in db.get_all_predictions():
        print(row)
