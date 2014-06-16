#!/usr/bin/python

# From this SO answer http://stackoverflow.com/a/2020553/212224

import smtplib
import configparser

# config = configparser.ConfigParser()
# config.read('emailconf.ini')

class EmailNotifier:

	config = configparser.ConfigParser()
	config.read('emailconf.ini')

	def notify(self, subject, body):

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
		server.set_debuglevel(3)
		server.login(USER, PASS)
		server.sendmail(FROM, TO, self.compose(FROM, TO, subject, body))
		server.quit()

	def compose(self, FROM, TO, subject, body):

		header  = 'From: %s\n' % FROM
		header += 'To: %s\n' % ','.join(TO)
		# header += 'Cc: %s\n' % ','.join(cc_addr_list)
		header += 'Subject: %s\n\n' % subject
		message = header + message

		return message

eNotify = EmailNotifier()
eNotify.notify("Snapshot script failed!", "The script failed. You should investigate.")