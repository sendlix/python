from src.sendlix.clients import EmailClient

client = EmailClient(
    "sk_qrdejoofltl4lx7r4hu1n5o5hakmmjqs6uxrd3vu1tfj9c0dg9icektv60uqgawp.5724316020768768")


res = client.send_email(
    mail_options={
        "from": "info@sendlix.com",
        "to": ["sebastian.brunow@gmail.com"],
        "subject": "Hello from the Python SDK",
        "html": "<h1>It works!</h1><p>This email was sent using the Sendlix Python SDK.</p>",
        "text": "It works! This email was sent using the Sendlix Python SDK.",
    }
)

print(res)
