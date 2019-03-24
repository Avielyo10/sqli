#!/usr/bin/env python

import sys
import urllib2

import time
import datetime

import tqdm

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool


MOODLE_PREFIX = "https://moodlearn.ariel.ac.il/course/index.php?categoryid="
MOODLE_POSTFIX = "&browse=courses&perpage=10000&page=0"
TEST = MOODLE_PREFIX+'877'+MOODLE_POSTFIX
LINKS = set()
URLS = []

"""
What I did to improve the efficiency is to iterate all the categories
with all the possible courses,to achieve that I chose this
prefix `&browse=courses&perpage=10000&page=0`,
this will guarantee having all the courses on the same page from a certain category.

If course is open, there is an "unlock" symbol next to it.
So instead of iterating on each and every course, I looked on the overall
page, and look for this symbol, if found - return the link to it.
"""


def init_urls():
    for category_id in range(126, 1013):
        tmp_url = MOODLE_PREFIX+str(category_id)+MOODLE_POSTFIX
        URLS.append(tmp_url)


def add_links(soup):
    for i in soup.find_all('div', {'class': 'info'}):
        for _ in i.find_all('i', {'class': 'icon fa fa-unlock-alt fa-fw'}):
            link = i.find_all('a')[0].get('href')
            LINKS.add(link)


def write_to_output(links):
    with open("output.out", "w+") as output:
        for link in links:
            output.write(link+"\n")


def summary():
    print "\n=== SUMMARY ==="
    for link in LINKS:
        print link


def job(url):
    try:
        html_doc = urllib2.urlopen(url)
        soup = BeautifulSoup(html_doc, 'lxml')
        add_links(soup)
    except:
        pass


def test_case():
    print "\n=== TEST START ==="
    try:
        print "Currently on " + TEST
        print "=========="
        job(TEST)
    except:
        print "[TEST Error] " + TEST

    for link in LINKS:
        print link
    LINKS.clear()
    print "=== TEST END ===\n"


def main():
    init_urls()
    for _ in tqdm.tqdm(ThreadPool(8).imap_unordered(job, URLS), total=len(URLS), desc="Processing Categories"):
        pass

    # Adding MOODLE 101
    LINKS.add("https://moodlearn.ariel.ac.il/course/view.php?id=2")
    write_to_output(LINKS)


def entry_point():
    if "-t" in sys.argv[1:]:
        test_case()

    with_summary = False
    if "-w" in sys.argv[1:]:
        with_summary = True

    # Get elapsed time.
    start_time = time.time()
    
    main()
    if with_summary:
        summary()
    print "\nFinished in {}.".format(
        datetime.timedelta(seconds=(time.time()-start_time)))
