def send_email(to, *, subject, body):
    """Sends an email. subject and body are keyword-only."""
    print(f"To: {to}, Subject: {subject}, Body: {body}")

send_email("user@example.com", subject="Important Update", body="Check out the latest news!")
# Output: To: user@example.com, Subject: Important Update, Body: Check out the latest news!

try:
    send_email("user@example.com", "Important Update", "Check out the latest news!")
except TypeError as e:
    print(f"Error: {e}")
    # Output: Error: send_email() takes 1 positional argument but 3 were given