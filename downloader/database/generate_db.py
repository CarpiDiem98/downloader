import sqlite3

# Crea una connessione al database SQLite (questo creerà il file del database se non esiste)
conn = sqlite3.connect("annotations.db")

# Crea un cursore per eseguire comandi SQL
c = conn.cursor()

# Crea una tabella per memorizzare le annotazioni
c.execute(
    """
    CREATE TABLE IF NOT EXISTS annotations (
        id INTEGER PRIMARY KEY,
        title TEXT,
        url TEXT NOT NULL UNIQUE
    )
"""
)
conn.commit()
conn.close()
