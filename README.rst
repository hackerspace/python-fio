Fio scraper
===========

Fio bank [http://fio.cz] transparent account data scraper.

Requirements:
 - python >= 2.7
 - python-lxml >= 2.3

Usage:
 - import fio
 - url = ('https://www.fio.cz/scgi-bin/hermes/dz-transparent.cgi?ID_ucet=%d'
        % account_num)
 - data = fio.scrape(url)

Sample output:
--------------

$ ./fio/scrape.py | tail -n 5 ::

        2012-05-20   -1796.00
        2012-05-22    -900.00
        2012-05-24    -400.00
        2012-05-31       1.50
        2012-06-01  -10028.00
