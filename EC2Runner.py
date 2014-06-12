#!/usr/bin/python

import logging
import logging.config
import configparser

from EC2VolumeSnapshotter import EC2VolumeSnapshotter

logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('config.ini')

volumes = []
for key in config['volumes']:
	volumes.append(config['volumes'][key])

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

region = 'eu-west-1'
ec2vs = EC2VolumeSnapshotter(region)

logger.info("Beginning script with region: " + region)

for volume in volumes:
	logger.info('Snapshotting volume: ' + volume)
	ec2vs.runSnapshotter(volume)