#!/usr/bin/python

# From this SO answer http://stackoverflow.com/a/2020553/212224

import smtplib

SERVER = "localhost"
FROM = ""
TO = [""]
SUBJECT = "Alert!"
TEXT = "This message was sent with Python's smtplib."


message = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

server = smtplib.SMTP(SERVER)
server.set_debuglevel(3)
server.sendmail(FROM, TO, message)
server.quit()