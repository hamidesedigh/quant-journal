import sqlite3

DB_NAME = "reports.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

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

    conn.commit()
    conn.close()