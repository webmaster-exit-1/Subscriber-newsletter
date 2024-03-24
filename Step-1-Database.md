Step 1: Database Setup

We'll use SQLite as our database system for simplicity and ease of use. Let's design the database schema to store subscriber information, newsletter content, and other relevant data.

Here's the proposed database schema:

```sql
-- Table: subscribers
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    name TEXT,
    subscribed INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: newsletters
CREATE TABLE IF NOT EXISTS newsletters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    body TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scheduled_at TIMESTAMP
);

-- Table: newsletter_subscribers
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    newsletter_id INTEGER,
    subscriber_id INTEGER,
    sent_at TIMESTAMP,
    opened_at TIMESTAMP,
    FOREIGN KEY (newsletter_id) REFERENCES newsletters (id),
    FOREIGN KEY (subscriber_id) REFERENCES subscribers (id)
);
```

Now, let's implement the database creation and connection functionality in Python:

```python
import sqlite3

def create_tables():
    conn = sqlite3.connect('newsletter.db')
    c = conn.cursor()

    # Create subscribers table
    c.execute('''CREATE TABLE IF NOT EXISTS subscribers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT UNIQUE,
                 name TEXT,
                 subscribed INTEGER DEFAULT 1,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # Create newsletters table
    c.execute('''CREATE TABLE IF NOT EXISTS newsletters
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 subject TEXT,
                 body TEXT,
                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 scheduled_at TIMESTAMP)''')

    # Create newsletter_subscribers table
    c.execute('''CREATE TABLE IF NOT EXISTS newsletter_subscribers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 newsletter_id INTEGER,
                 subscriber_id INTEGER,
                 sent_at TIMESTAMP,
                 opened_at TIMESTAMP,
                 FOREIGN KEY (newsletter_id) REFERENCES newsletters (id),
                 FOREIGN KEY (subscriber_id) REFERENCES subscribers (id))''')

    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('newsletter.db')
    return conn
```

In the `create_tables()` function, we execute the SQL statements to create the necessary tables if they don't already exist. The `get_db_connection()` function establishes a connection to the SQLite database and returns the connection object.

Make sure to call the `create_tables()` function when initializing your program to ensure that the required tables are created.
With the database setup complete, we can move on to the next step: Email Configuration.
