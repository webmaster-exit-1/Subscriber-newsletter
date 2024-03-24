Step 5: Unsubscribe and GDPR Compliance

In this step, we'll implement an unsubscribe mechanism, allowing users to opt-out of receiving newsletters. We'll also ensure GDPR compliance by providing necessary information and obtaining user consent.

Here's the code for unsubscribe and GDPR compliance:

```python
def generate_unsubscribe_link(subscriber_id):
    # Generate a unique unsubscribe link for the subscriber
    unsubscribe_token = generate_token(subscriber_id)
    unsubscribe_link = f"http://example.com/unsubscribe?token={unsubscribe_token}"
    return unsubscribe_link

def generate_token(subscriber_id):
    # Generate a secure token for the subscriber
    # You can use a library like itsdangerous or implement your own token generation logic
    # For simplicity, we'll use a plain subscriber ID as the token
    return str(subscriber_id)

def process_unsubscribe_request(token):
    # Verify the unsubscribe token and unsubscribe the subscriber
    subscriber_id = verify_token(token)
    if subscriber_id:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE subscribers SET subscribed = 0 WHERE id = ?", (subscriber_id,))
        conn.commit()
        conn.close()
        print(f"Subscriber {subscriber_id} unsubscribed successfully.")
    else:
        print("Invalid unsubscribe token.")

def verify_token(token):
    # Verify the token and return the subscriber ID if valid
    # You can use a library like itsdangerous or implement your own token verification logic
    # For simplicity, we'll assume the token is a plain subscriber ID
    try:
        subscriber_id = int(token)
        return subscriber_id
    except ValueError:
        return None

def send_newsletter_with_unsubscribe_link(newsletter_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM newsletters WHERE id = ?", (newsletter_id,))
    newsletter = c.fetchone()

    if newsletter:
        subject, body, _, scheduled_at = newsletter
        subscribers = get_subscribed_subscribers()

        for subscriber in subscribers:
            subscriber_id, email, name, _, _ = subscriber
            unsubscribe_link = generate_unsubscribe_link(subscriber_id)
            personalized_body = body.replace('{name}', name)
            personalized_body += f'<br><a href="{unsubscribe_link}">Unsubscribe</a>'
            email_config.send_email(subject, personalized_body, [email])
            c.execute("INSERT INTO newsletter_subscribers (newsletter_id, subscriber_id, sent_at) VALUES (?, ?, ?)",
                      (newsletter_id, subscriber_id, datetime.now()))

        conn.commit()
        print(f"Newsletter {newsletter_id} sent to {len(subscribers)} subscribers with unsubscribe links.")
    else:
        print(f"Newsletter {newsletter_id} not found.")

    conn.close()
```

The unsubscribe and GDPR compliance functions include:

- `generate_unsubscribe_link(subscriber_id)`: Generates a unique unsubscribe link for a subscriber based on their ID. In this example, we assume the link is in the format `http://example.com/unsubscribe?token={unsubscribe_token}`.

- `generate_token(subscriber_id)`: Generates a secure token for the subscriber. For simplicity, we use the plain subscriber ID as the token, but in a real-world scenario, you should use a secure token generation library or implement your own token generation logic.

- `process_unsubscribe_request(token)`: Processes an unsubscribe request by verifying the provided token and unsubscribing the corresponding subscriber if the token is valid.

- `verify_token(token)`: Verifies the token and returns the subscriber ID if
