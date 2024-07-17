# email_utils.py

from dotenv import load_dotenv
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Load environment variables
load_dotenv()

# Environment variables for email credentials
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Check if environment variables are loaded correctly
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    raise ValueError("Email address or password environment variables are not set.")

def email_user(email, name, message):
    funny_images = ["fitness.jpg", "fitness1.jpg", "fitness2.jpg", "fitness3.jpg"]
    random_img = random.randint(0, len(funny_images) - 1)
    attachment_path = funny_images[random_img]

    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = email
        msg['Subject'] = "Performance Summary"

        # Attach the body with the msg instance
        greeting = f"<p style=\"font-size:30px; text-align: center; color:Red;\"> <b>Amazing Workout {name}! </b> </p> <br>"
        performance_summary = f"<p style=\"font-size:20px; text-align: center;\"><b>Here is your Performance Summary<b>:<br><br>{message}</p>"
        msg.attach(MIMEText(greeting + performance_summary, 'html'))

        # Attach the file
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f"attachment; filename= {os.path.basename(attachment_path)}",
                )
                msg.attach(part)

        # Create the SMTP session
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Login to the email server

            # Send the email
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, email, text)

        print(f"Email sent successfully to {email}")

    except Exception as e:
        print(f"Error creating or sending email: {e}")


def main():
    # Replace with your desired message content
    message = "This is your performance summary message. You can add more details and personalize it further."
    email_user("o190228@rguktong.ac.in", "Priya", message)

if __name__ == "__main__":
    main()

