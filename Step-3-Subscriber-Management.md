Step 3: Subscriber Management

In this step, we'll develop functions to add new subscribers, unsubscribe existing subscribers, and update subscriber preferences. We'll also implement database queries and operations for subscriber management.

Here's the code for subscriber management:

```python
def add_subscriber(email, name):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO subscribers (email, name) VALUES (?, ?)", (email, name))
        conn.commit()
        print(f"Subscriber {email} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Subscriber {email} already exists.")
    finally:
        conn.close()

def unsubscribe_subscriber(email):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE subscribers SET subscribed = 0 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    print(f"Subscriber {email} unsubscribed successfully.")

def update_subscriber_name(email, new_name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE subscribers SET name = ? WHERE email = ?", (new_name, email))
    conn.commit()
    conn.close()
    print(f"Subscriber {email} name updated to {new_name}.")

def get_subscribed_subscribers():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM subscribers WHERE subscribed = 1")
    subscribers = c.fetchall()
    conn.close()
    return subscribers

# Usage examples
add_subscriber('john@example.com', 'John Doe')
unsubscribe_subscriber('john@example.com')
update_subscriber_name('john@example.com', 'John Smith')
subscribed_subscribers = get_subscribed_subscribers()
```

The subscriber management functions include:

- `add_subscriber(email, name)`: Adds a new subscriber to the database with the provided email and name. If the email already exists, it prints an error message.

- `unsubscribe_subscriber(email)`: Unsubscribes a subscriber by setting their `subscribed` status to 0 in the database.

- `update_subscriber_name(email, new_name)`: Updates the name of a subscriber in the database based on their email.

- `get_subscribed_subscribers()`: Retrieves all subscribed subscribers from the database.

These functions interact with the database using SQL queries to perform the necessary operations.

With the subscriber management functionality in place, we can add new subscribers, unsubscribe them, update their preferences, and retrieve the list of subscribed subscribers.

In the next step, we'll focus on newsletter creation and sending, where we'll implement functions to compose and store newsletter content, and send newsletters to subscribed users.
