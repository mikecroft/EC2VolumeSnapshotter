#!/usr/bin/python

import logging
import logging.config

from EC2VolumeSnapshotter import EC2VolumeSnapshotter

logger = logging.getLogger(__name__)

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

region = 'eu-west-1'
volumes = ['vol-08f84a0a']
ec2vs = EC2VolumeSnapshotter(region)

logger.info("Beginning script with region: " + region)

for volume in volumes:
	logger.info('Snapshotting volume: ' + volume)
	ec2vs.runSnapshotter(volume)