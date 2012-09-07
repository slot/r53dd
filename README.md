Route53 Dynamic DNS
===================

Route53 dynamic dns updater written in Python

If you are using Amazon's Route53 DNS Service and want to connect a box at home, this one is for you. The script
will determine your current IP address and update your Route53 hosted zone record if necessary.

It will also create a new record if non exists under the hostename. If no hostename was configured it will by default
use the systems hostname.

Dependencies
=============

The updater is using the Boto project, a python interface to Amazon Web Services.
Please download and install Boto from here: https://github.com/boto/boto

How to set it up
================

Clone it on your system:
```sh
git clone https://github.com/slot/r53dd
```

Configure AWS keys and hosted_zone etc. in r53dd/updater.cfg (see documentation inside file)

Run the r53dd updater
=====================

```sh
python r53dd
```

Create a cronjob to check and update your IP automatically:

Example:

```sh
# crontab
*/5 * * * * /usr/bin/python /home/slot/r53dd > /home/slot/r53dd.log
```

