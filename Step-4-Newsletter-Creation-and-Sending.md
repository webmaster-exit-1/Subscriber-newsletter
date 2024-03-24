Step 4: Newsletter Creation and Sending

In this step, we'll create a system for composing and storing newsletter content, including the subject, body, and any attachments. 
We'll also implement functions to send newsletters to subscribed users, handling personalization and dynamic content.

Here's the code for newsletter creation and sending:

```python
def create_newsletter(subject, body, scheduled_at=None):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO newsletters (subject, body, scheduled_at) VALUES (?, ?, ?)", (subject, body, scheduled_at))
    newsletter_id = c.lastrowid
    conn.commit()
    conn.close()
    print(f"Newsletter {newsletter_id} created successfully.")
    return newsletter_id

def send_newsletter_to_subscribers(newsletter_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM newsletters WHERE id = ?", (newsletter_id,))
    newsletter = c.fetchone()

    if newsletter:
        subject, body, _, scheduled_at = newsletter
        subscribers = get_subscribed_subscribers()

        for subscriber in subscribers:
            subscriber_id, email, name, _, _ = subscriber
            personalized_body = body.replace('{name}', name)
            email_config.send_email(subject, personalized_body, [email])
            c.execute("INSERT INTO newsletter_subscribers (newsletter_id, subscriber_id, sent_at) VALUES (?, ?, ?)",
                      (newsletter_id, subscriber_id, datetime.now()))

        conn.commit()
        print(f"Newsletter {newsletter_id} sent to {len(subscribers)} subscribers.")
    else:
        print(f"Newsletter {newsletter_id} not found.")

    conn.close()

# Usage examples
newsletter_id = create_newsletter("Weekly Update", "<h1>Hello, {name}!</h1><p>Here's your weekly update.</p>")
send_newsletter_to_subscribers(newsletter_id)
```

The newsletter creation and sending functions include:

- `create_newsletter(subject, body, scheduled_at=None)`:
- Creates a new newsletter in the database with the provided subject, body, and optional scheduled sending time.
- It returns the ID of the newly created newsletter.

- `send_newsletter_to_subscribers(newsletter_id)`:
- Retrieves the newsletter from the database based on the provided `newsletter_id`.
- If the newsletter exists, it retrieves the list of subscribed subscribers and sends the newsletter to each subscriber individually.
- It personalizes the newsletter body by replacing the `{name}` placeholder with the subscriber's name. It also records the sending information in the `newsletter_subscribers` table.

These functions interact with the database to store and retrieve newsletter content and subscriber information. 
The `send_newsletter_to_subscribers()` function uses the `email_config` object from the previous step to send emails to subscribers.
With the newsletter creation and sending functionality in place, we can compose newsletters, store them in the database, and send them to subscribed users with personalized content.
In the next step, we'll implement the unsubscribe mechanism and ensure GDPR compliance by providing necessary information and obtaining user consent.
