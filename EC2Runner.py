#!/usr/bin/python

import logging
import logging.config

from EC2VolumeSnapshotter import EC2VolumeSnapshotter

logger = logging.getLogger(__name__)

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

ec2_home = ""
path = ""
java_home = ""
region = 'eu-west-1'
aws_access_key = ''
aws_secret_key = ''


ec2vs = EC2VolumeSnapshotter(ec2_home, 
				 path, java_home, region,
				 aws_access_key, aws_secret_key)


#logger.info("trying with vol-00000123")

#ec2vs.isVolNameValid("vol-00000123")

logger.info("validating vol-08f84a0a")
ec2vs.isVolNameValid("vol-08f84a0a")

#logger.info("trying to create snapshot")
#ec2vs.createSnapshot("vol-08f84a0a")

logger.info("listing snapshots for vol-08f84a0a")
logger.info(ec2vs.listSnapshots("vol-08f84a0a"))

