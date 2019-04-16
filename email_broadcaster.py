import csv, smtplib, ssl
import sys

message = """Subject: Time-Tracking System Testing

Hi, {name} {surname}, 

The group B17-05-4 is glad to invite you to the testing of the project Time-Tracking System.

The host of the website is: {host}
Here are your credentials to login into the system:
Login: {email}
Password: {pwd}

We suggest you to change your password as soon as you enter to the system in Profile page.

Should you have any questions or feedback, please, write us in Telegram.
Yours sincerely,
YATracker Team
"""
from_address = "yatracker.team@gmail.com"
password = input("Type your password and press enter: ")
host = "http://138.68.108.57:8000"


def send_mails(filename):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_address, password)
        with open(filename) as file:
            reader = csv.reader(file)
            next(reader)
            for _, surname, name, email, pwd, _ in reader:
                server.sendmail(
                    from_address,
                    email,
                    message.format(name=name, surname=surname, host=host, email=email, pwd=pwd),
                )
    print("Emails are sent!")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        send_mails(sys.argv[1])
