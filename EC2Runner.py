#!/usr/bin/python

import logging
import logging.config
import configparser

from EC2VolumeSnapshotter import EC2VolumeSnapshotter

logger = logging.getLogger(__name__)
logging.config.fileConfig('logging.ini', disable_existing_loggers=False)


config = configparser.ConfigParser()
config.read('config.ini')

# volumes = []
region = 'eu-west-1'
ec2vs = EC2VolumeSnapshotter()

for key in config.sections():
	logger.info('Snapshotting ' + key)
	logger.info('Maintaining ' + config[key]['ssmin'] + ' snapshots')

	ec2vs.runSnapshotter(
		config[key]['vol_name'],
		int(config[key]['ssmin']),
		config[key]['region'])
