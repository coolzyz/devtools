#!/usr/bin/env python2
# encoding utf8

import re
import math
import urllib2

#tai guo
_CHINA_SUBNETS_FILE = "/tmp/tai_subnets.txt"
_ALLOC_APNIC_URL = (
    r'http://ftp.apnic.net'
    r'/apnic/stats/apnic/delegated-apnic-latest')


def apnic_record_to_net(record):
    unit_items = record.split('|')
    starting_ip, num_ip = unit_items[3], int(unit_items[4])

    imask = 0xffffffff ^ (num_ip - 1)
    imask = hex(imask)[2:]

    mask = [0] * 4
    mask[0] = imask[0:2]
    mask[1] = imask[2:4]
    mask[2] = imask[4:6]
    mask[3] = imask[6:8]

    mask = [int(i, 16) for i in mask]
    mask = "%d.%d.%d.%d" % tuple(mask)
    mask2 = 32 - int(math.log(num_ip, 2))

    return (starting_ip, mask, mask2)


def get_china_subnets_from_apnic():
    '''fetch ip allocation data from apnic
    '''

    china_subnets = []

    print ("Fetching data from apnic.net, "
           "it might take a few minutes, please wait...")

    china_regex = re.compile(
            r'apnic\|TH\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',
            re.IGNORECASE)

    apnic_alloc = urllib2.urlopen(_ALLOC_APNIC_URL).read()
    records_china = china_regex.findall(apnic_alloc)

    for record in records_china:
        china_subnets.append(apnic_record_to_net(record))

    return china_subnets


def write_subnets_to_file(china_subnets):
    china_subnets_file = open(_CHINA_SUBNETS_FILE, 'w')

    for (net, mask, mask2) in china_subnets:
        china_subnets_file.write("%s/%s," % (net, mask2))

    print "%s generated." % _CHINA_SUBNETS_FILE


if __name__ == "__main__":
    write_subnets_to_file(get_china_subnets_from_apnic())
