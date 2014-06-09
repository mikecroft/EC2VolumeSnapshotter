import logging
import logging.config

from EC2VolumeSnapshotter import EC2VolumeSnapshotter

logger = logging.getLogger(__name__)

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

ec2_home = ""
path = ""
java_home = ""
region = 'eu-west-1'
aws_access_key = 'AKIAI2SFGZYDFCR2QFRQ'
aws_secret_key = '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'


ec2vs = EC2VolumeSnapshotter(ec2_home, 
				 path, java_home, region,
				 aws_access_key, aws_secret_key)

logger.info(ec2vs.createSnapshot(""))

logger.info("trying with vol-00000123")

ec2vs.isVolNameValid("vol-00000123")

logger.info("trying again with vol-08f84a0a")
ec2vs.isVolNameValid("vol-08f84a0a")

logger.info("trying to create snapshot")
ec2vs.createSnapshot("vol-08f84a0")




#ec2addsnap -O AKIAI2SFGZYDFCR2QFRQ -W YLBiIUgTLtyWJF85pOxqPDid8WQMbDl6/Duckokg --region eu-west-1 vol-08f84a0