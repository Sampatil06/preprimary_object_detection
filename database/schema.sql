CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    image_path TEXT,
    detected_objects TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
