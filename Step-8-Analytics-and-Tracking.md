Step 8: Analytics and Tracking

In this step, we'll integrate analytics and tracking features to measure the performance of newsletters and gather valuable insights. We'll track open rates, click-through rates, and other relevant metrics.

Here's an example of how you can implement analytics and tracking:

```python
from urllib.parse import urlencode

def generate_tracking_link(subscriber_id, newsletter_id, link):
    tracking_params = {
        'subscriber_id': subscriber_id,
        'newsletter_id': newsletter_id
    }
    tracking_query = urlencode(tracking_params)
    tracking_link = f"http://example.com/track?{tracking_query}&url={link}"
    return tracking_link

def process_tracking_request(subscriber_id, newsletter_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE newsletter_subscribers SET opened_at = ? WHERE subscriber_id = ? AND newsletter_id = ?",
              (datetime.now(), subscriber_id, newsletter_id))
    conn.commit()
    conn.close()

def send_newsletter_with_tracking(newsletter_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM newsletters WHERE id = ?", (newsletter_id,))
    newsletter = c.fetchone()

    if newsletter:
        subject, body, _, scheduled_at = newsletter
        subscribers = get_subscribed_subscribers()

        for subscriber in subscribers:
            subscriber_id, email, name, _, _ = subscriber
            tracking_pixel_url = generate_tracking_link(subscriber_id, newsletter_id, '')
            tracking_pixel = f'<img src="{tracking_pixel_url}" width="1" height="1" alt="">'
            personalized_body = body.replace('{name}', name)
            personalized_body += tracking_pixel
            email_config.send_email(subject, personalized_body, [email])
            c.execute("INSERT INTO newsletter_subscribers (newsletter_id, subscriber_id, sent_at) VALUES (?, ?, ?)",
                      (newsletter_id, subscriber_id, datetime.now()))

        conn.commit()
        print(f"Newsletter {newsletter_id} sent to {len(subscribers)} subscribers with tracking.")
    else:
        print(f"Newsletter {newsletter_id} not found.")

    conn.close()

def get_newsletter_analytics(newsletter_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM newsletter_subscribers WHERE newsletter_id = ?", (newsletter_id,))
    total_sent = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM newsletter_subscribers WHERE newsletter_id = ? AND opened_at IS NOT NULL", (newsletter_id,))
    total_opened = c.fetchone()[0]
    conn.close()

    open_rate = (total_opened / total_sent) * 100 if total_sent > 0 else 0
    return {
        'total_sent': total_sent,
        'total_opened': total_opened,
        'open_rate': open_rate
    }
```

In this example, we introduce tracking functionality and analytics:

- `generate_tracking_link(subscriber_id, newsletter_id, link)`: This function generates a unique tracking link for each subscriber and newsletter combination. It appends tracking parameters (`subscriber_id` and `newsletter_id`) to the provided `link` URL.

- `process_tracking_request(subscriber_id, newsletter_id)`: This function is called when a tracking link is clicked or a tracking pixel is loaded. It updates the `opened_at` timestamp in the `newsletter_subscribers` table to record the opening of the newsletter by the subscriber.

- `send_newsletter_with_tracking(newsletter_id)`: This function sends the newsletter with tracking capabilities. It includes a tracking pixel in the newsletter body, which is a small transparent image with a unique tracking URL. When the newsletter is opened and the tracking pixel is loaded, it triggers the `process_tracking_request()` function to record the opening event.

- `get_newsletter_analytics(newsletter_id)`: This will retrieve the analytics data for the newsletter with ID 1 and print the total sent, total opened, and open rate.

With the `get_newsletter_analytics()` function completed, you now have a way to retrieve and analyze the performance metrics of your newsletters.

- `get_newsletter_analytics(newsletter_id)`: This function retrieves analytics data for a specific newsletter. It performs the following
steps:
  1. It establishes a connection to the database using `get_db_connection()`.
  2. It executes a SQL query to count the total number of subscribers to whom the newsletter was sent, using the `newsletter_id`.
  3. It executes another SQL query to count the number of subscribers who opened the newsletter, by checking the `opened_at` timestamp in the `newsletter_subscribers` table.
  4. It calculates the open rate percentage by dividing the total opened count by the total sent count and multiplying by 100. If the total sent count is 0, it sets the open rate to 0 to avoid division by zero.
  5. It returns a dictionary containing the analytics data, including the total sent count, total opened count, and open rate percentage.

You can use the `get_newsletter_analytics(newsletter_id)` function to retrieve analytics data for a specific newsletter and display it in your web interface or generate reports.

For example, you can call the function like this:

```python
newsletter_id = 1
analytics_data = get_newsletter_analytics(newsletter_id)
print(f"Analytics for Newsletter {newsletter_id}:")
print(f"Total Sent: {analytics_data['total_sent']}")
print(f"Total Opened: {analytics_data['total_opened']}")
print(f"Open Rate: {analytics_data['open_rate']}%")
```

This will retrieve the analytics data for the newsletter with ID 1 and print the total sent count, total opened count, and open rate percentage.

With the analytics and tracking functionality in place, you can gain valuable insights into the performance of your newsletters, track user engagement, and make data-driven decisions to improve your email campaigns.
