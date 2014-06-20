#!/usr/bin/python

import smtplib,configparser,email,email.encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class EmailNotifier:

	config = configparser.ConfigParser()
	config.read('emailconf.ini')

	def notify(self, subject, body, attachment = None):

		SERVER = self.config['Sender']['SERVER']
		USER = self.config['Sender']['USER']
		PASS = self.config['Sender']['PASS']
		FROM = self.config['Sender']['FROM']
		TO = []
		SUBJECT = subject
		TEXT = body

		for addr in self.config['Notify_List']:
			TO.append(self.config['Notify_List'][addr])

		server = smtplib.SMTP(SERVER, 587)
		server.starttls()
		server.set_debuglevel(3)
		server.login(USER, PASS)
		if (attachment is None):
			server.sendmail(FROM, TO, self.compose(FROM, TO, subject, body))
		else:
			server.sendmail(FROM, TO, self.composeWithLog(FROM, TO, subject, body, attachment).as_string())
		server.quit()

	def compose(self, FROM, TO, subject, body):

		# message = ""

		header  = 'From: %s\n' % FROM
		header += 'To: %s\n' % ','.join(TO)
		# header += 'Cc: %s\n' % ','.join(cc_addr_list)
		header += 'Subject: %s\n\n' % subject
		message = header + body

		return message

	def composeWithLog(self, FROM, TO, subject, body, attachment):

		# create html email
		html = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" '
		html +='"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">'
		html +='<body style="font-size:12px;font-family:Verdana"><p>'
		html += "<br />".join(body.split("\n"))
		html += "</p></body></html>"
		emailMsg = MIMEMultipart('mixed')
		emailMsg['Subject'] = subject
		emailMsg['From'] = FROM
		emailMsg['To'] = ', '.join(TO)
		emailMsg.attach(MIMEText(html,'html'))

		# now attach the file
		fileMsg = MIMEBase('application','octet-stream')
		fileMsg.set_payload(open(attachment, 'r').read())
		email.encoders.encode_base64(fileMsg)
		fileMsg.add_header('Content-Disposition','attachment;filename='+attachment)
		emailMsg.attach(fileMsg)

		return emailMsg