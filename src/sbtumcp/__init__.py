conn.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
""")
conn.commit()