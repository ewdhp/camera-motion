import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_gmail_email(sender_email, sender_password, receiver_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")
        return True, "Email sent successfully!"
    except Exception as e:
        print(f"Error sending email: {e}")
        return False, f"Error sending email: {e}"

# Credentials:
sender_email = "ewd2955@gmail.com"  # Replace with your Gmail address
sender_password = "rqdk hltu zqqj lgdu"  # Your app password
receiver_email = "ewd2955@gmail.com"  # Replace with the recipient's email
subject = "Gmail Email Test"
body = "This is a test email sent using Gmail and an app password."

success, message = send_gmail_email(sender_email, sender_password, receiver_email, subject, body)

if success:
    print(message)
else:
    print(message)