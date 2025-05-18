import duckdb
from pathlib import Path
from .config import settings

class Database:
    def __init__(self):
        db_path = Path(settings.DB_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = duckdb.connect(str(db_path))
        self._init_tables()

    def _init_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            paper_id VARCHAR PRIMARY KEY,
            title VARCHAR,
            abstract TEXT,
            source_type VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS figures (
            figure_id VARCHAR PRIMARY KEY,
            paper_id VARCHAR,
            caption TEXT,
            url VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            entity_id VARCHAR PRIMARY KEY,
            figure_id VARCHAR,
            entity_type VARCHAR,
            entity_text VARCHAR,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (figure_id) REFERENCES figures(figure_id)
        )
        """)

db = Database()