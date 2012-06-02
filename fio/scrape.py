#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Simple web scraper for Fio bank public accounts

import sys
import urllib
import lxml.html

import datetime
import unicodedata

class dotdict(dict):
    """ Dictionary with dot access """
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


def scrape(url):
    """ Scrape Fio webpage """

    content = urllib.urlopen(url).read()
    root = lxml.html.fromstring(content)

    def sanitize_amount(inp):
        return float(inp.replace(',', '.').replace(' ',''))

    def sanitize_symbol(inp):
        if inp.isdigit():
            return int(inp)
        return 0

    data = []

    for table in root.cssselect("table.main"):
        for table_row in reversed(table.cssselect("tr")[1:-1]):
            plain_row = map(lambda x: x.text_content(), table_row)
            raw = map(lambda x: x.replace(u'\xa0', u''), plain_row)

            item = dotdict()
            item.amount = sanitize_amount(raw[1])
            item.payment_type = raw[2]
            item.ks = sanitize_symbol(raw[3])
            item.vs = sanitize_symbol(raw[4])
            item.ss = sanitize_symbol(raw[5])
            item.identification = raw[6]
            item.message = raw[7]

            date = map(lambda x: int(x), raw[0].split('.'))
            item.arrival = datetime.date(day=date[0], month=date[1],
                year=date[2])

            data.append(item)

    return data

if __name__ == "__main__":

    # usage example:

    url = 'https://www.fio.cz/scgi-bin/hermes/dz-transparent.cgi?' \
        'pohyby_DAT_od=01.01.2011&ID_ucet=2900086515'

    for item in scrape(url):
        print '%s %s' % (item.arrival,
            ('% .2f' % item.amount).rjust(10))
