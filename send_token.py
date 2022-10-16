import smtplib, ssl
import sys
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser(interpolation=None)
config.read(file)

## import system variables
if len(sys.argv) > 1:
    debug = str(sys.argv[1])
    reg_username = str(sys.argv[2])
    reg_name = str(sys.argv[3])
    reg_mail = str(sys.argv[4])
    token = str(sys.argv[5])
    if debug == "debug":
        debug = True
else:
    debug = False

## define webserver ports for SMTP
port = 465  # For SSL
password = str(config['credentials']['password_web'])

## define host for mailserver
smtp_server = "cap.ssl.hosttech.eu"

## account is setup on webserver
sender_email = "no_reply@ksrminecraft.ch"
receiver_email = f"{reg_mail}" ## improted system variable
message = f"""\
Subject: Deine Registration bei KSRMinecraft

Hallo {reg_name}

Benutze bitte folgenden Token für deine Registrierung:

{token}

Bitte antworte nicht auf diese E-Mail."""

if debug:
    print("SENDING:")
    print(reg_mail)
    print(token)
## Engine, that sends the mail. Problem: Potential Spam-Filter
context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
