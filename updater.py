#/usr/bin/python
from boto import route53
import httplib
import socket
import re

class r53dd:

    def __init__(self, hosted_zone, aws_key, aws_secret, ip_source, ttl = 300, hostname = None):
        """
        Init Route53 DynDns Client

        :type hosted_zone: str
        :param hosted_zone: The domain name managed by Route53

        :type aws_key: str
        :param aws_key: AWS key from security credentials

        :type aws_secret: str
        :param aws_secret: AWS secret from security credentials

        :type ttl: int
        :param ttl: domain time to live in seconds, defaults to 300
        """

        if hosted_zone[-1] != ".":
            hosted_zone = hosted_zone + "."

        self.hosted_zone = hosted_zone
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        self.ip_source = ip_source
        self.ttl = ttl
        self.hostname = hostname

    def getR53Connection(self):
        """ Opens a connection to Amazon's Route53 service """
        return route53.Route53Connection(self.aws_key, self.aws_secret)


    def getHostedZone(self):
        """ get hosted_zone object by name """
        r53 = self.getR53Connection()
        zone = r53.get_hosted_zone_by_name(self.hosted_zone)

        if zone == None:
            print "Zone with name " + self.hosted_zone + " not found. Aborting."
            exit(1)

        """
        fix for current bug in boto library
        see https://github.com/boto/boto/issues/448
        """
        if zone.Id[0:12] == '/hostedzone/':
            zone.Id = zone.Id.replace('/hostedzone/', '')

        return zone


    def getRecords(self):
        """ get all records from configured zone """
        zone = self.getHostedZone()
        return self.getR53Connection().get_all_rrsets(zone.Id)


    def updateIp(self):
        """
        check if record exists. if no record exists create a record.
        if a record exists and ip address has changed delete it before
        new record being is created
        """
        records = self.getRecords()
        ip = self.getExternalIp()
        fqdn = self.getHostname() + '.' + self.hosted_zone

        for r in records:
            if (r.type == "A"):
                if (r.name == self.getHostname()+'.'+self.hosted_zone):
                    """ record exists """
                    """ return and do nothing if IP did not change """
                    old_ip = r.resource_records[0]
                    if old_ip == ip:
                        return

                    """if IP changed remove old record"""
                    change = records.add_change('DELETE', fqdn, 'A', self.ttl)
                    change.add_value(old_ip)

        """ create a a new record """
        change = records.add_change('CREATE', fqdn, 'A', self.ttl)
        change.add_value(ip)
        records.commit()

    def getExternalIp(self):
        """
        Retrieve external IP Address from service
        """
        ip = ''
        request_parts = self.ip_source.split("/", 1)
        print request_parts
        request_parts +=['']*(2-len(request_parts)) 
        (host, path) = request_parts
        print host
        print path
        iptest = httplib.HTTPConnection(host)
        iptest.request('GET', "/%s" % path)
        response = iptest.getresponse()

        if (response.status == 200):
            ip = re.search('((\d+\.){3}(\d+))', response.read()).group(0)

        iptest.close()

        """ if ip check worked run update record """
        if (len(ip) > 0):
            return ip

        return None

    def getHostname(self):
        """
        get configured hostname, if empty get hostname from sys
        """
        if self.hostname != None:
            return self.hostname

        return socket.gethostname().split('.')[0]

