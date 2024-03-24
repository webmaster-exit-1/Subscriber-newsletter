"""
This program uses SQLite to store subscriber information, including their email addresses and subscription status. 
It provides a simple command-line interface for managing newsletters and subscribers.

To use the program, you'll need to replace `'your_smtp_server'`, `'your_username'`, 
and `'your_password'` with your actual SMTP server details.

The program includes the following features:
1. Sending newsletters to subscribed users
2. Adding new subscribers
3. Unsubscribing users
4. GDPR compliance (users can unsubscribe, and their subscription status is stored in the database)

Please note that this is a basic implementation and may require additional features and improvements based on 
your specific requirements, such as handling bounced emails, providing a web interface for user sign-up and unsubscribe, 
and more advanced email templating.
"""


import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database setup
conn = sqlite3.connect('newsletter.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS subscribers
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             email TEXT UNIQUE,
             subscribed INTEGER)''')
conn.commit()

# Email configuration
smtp_server = 'your_smtp_server'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'

def send_email(subject, body, recipients):
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        for recipient in recipients:
            msg['To'] = recipient
            server.sendmail(smtp_username, recipient, msg.as_string())

def add_subscriber(email):
    try:
        c.execute("INSERT INTO subscribers (email, subscribed) VALUES (?, 1)", (email,))
        conn.commit()
        print(f"Subscriber {email} added successfully.")
    except sqlite3.IntegrityError:
        print(f"Subscriber {email} already exists.")

def remove_subscriber(email):
    c.execute("UPDATE subscribers SET subscribed = 0 WHERE email = ?", (email,))
    conn.commit()
    print(f"Subscriber {email} unsubscribed successfully.")

def get_subscribers():
    c.execute("SELECT email FROM subscribers WHERE subscribed = 1")
    return [row[0] for row in c.fetchall()]

def main():
    while True:
        print("\nNewsletter Management System")
        print("1. Send Newsletter")
        print("2. Add Subscriber")
        print("3. Unsubscribe")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            subject = input("Enter the newsletter subject: ")
            body = input("Enter the newsletter body (HTML): ")
            recipients = get_subscribers()
            send_email(subject, body, recipients)
            print("Newsletter sent successfully.")
        elif choice == '2':
            email = input("Enter the subscriber's email: ")
            add_subscriber(email)
        elif choice == '3':
            email = input("Enter the subscriber's email: ")
            remove_subscriber(email)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()
