#!/usr/bin/python3

import logging
import logging.config
import configparser

from EC2VolumeSnapshotter import EC2VolumeSnapshotter
from EmailNotifier import EmailNotifier

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
eNotify = EmailNotifier()

config = configparser.ConfigParser()
config.read('config.ini')


region = 'eu-west-1'
ec2vs = EC2VolumeSnapshotter()


try:
	for key in config.sections():
		logger.info('Snapshotting ' + key)
		logger.info('Maintaining ' + config[key]['ssmin'] + ' snapshots')

		ec2vs.runSnapshotter(
			config[key]['vol_name'],
			int(config[key]['ssmin']),
			config[key]['region'])
	pass
except Exception as e:
	logger.error('An error occurred: ' + str(e))
	eNotify.notify('Snapshot script failed!',
		'The script failed. You should investigate.\n' +
		'\nThe error was:\n' +
		str(e),
		'logs/snapshotter.log')
	raise e

eNotify.notify('Snapshot script completed without error!',
		'The script has finished.\nCheck the logs to see if it worked.' +
		'logs/snapshotter.log')