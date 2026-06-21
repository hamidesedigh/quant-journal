import sqlite3

# Database name for the report-analysis tables.
DB_NAME = "reports.db"


def get_connection():
    # Open a SQLite connection for report-related storage.
    return sqlite3.connect(DB_NAME)


def init_db():
    # Initialize the report database schema.
    conn = get_connection()
    cur = conn.cursor()

    # Daily report table: one high-level market report per date.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE,
        market_context TEXT,
        risk_regime TEXT,
        confidence INTEGER,
        hypothesis TEXT,
        probability INTEGER,
        invalidation TEXT,
        uncertainty TEXT,
        bias TEXT
    )
    """)

    # Asset analysis table: per-asset technical context linked to a report.
    cur.execute("""
    CREATE TABLE IF NOT EXISTS asset_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id INTEGER,
        asset TEXT,
        timeframe TEXT,
        trend TEXT,
        hh INTEGER,
        hl INTEGER,
        lh INTEGER,
        ll INTEGER,
        support REAL,
        resistance REAL,
        volume_level TEXT,
        volume_trend TEXT,
        liquidity TEXT,
        spread TEXT,
        FOREIGN KEY(report_id) REFERENCES daily_reports(id)
    )
    """)

    # Persist schema changes and close the connection.
    conn.commit()
    conn.close()
