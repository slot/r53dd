import updater
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('updater.cfg')

hosted_zone = config.get('settings', 'hosted_zone')
aws_key =  config.get('settings', 'aws_key')
aws_secret = config.get('settings', 'aws_secret')
ttl = config.get('settings', 'ttl')
hostname = config.get('settings', 'hostname')

if len(hostname) < 1:
    hostname = None

r53 = updater.r53dd(hosted_zone, aws_key, aws_secret, ttl, hostname)
r53.updateIp()

