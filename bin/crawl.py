#!/usr/bin/env python

import os, os.path, re
from BeautifulSoup import BeautifulSoup
from common import *

CITY = ['charlotte', 'denver', 'portland', 'tampa', 'minneapolis', 'stlouis']
CATG = ['cas', 'msr', 'm4m', 'm4w', 'w4m', 'w4w']

ROOT = None
SEEN = None

def main():
  lsRoot()
  lsSeen()
  openLog('crawl')
  for r in ROOT:
    crawlRoot(r)
  closeLog()

def lsRoot():
  global ROOT
  ROOT = []
  for city in CITY:
    for catg in CATG:
      r = 'http://%s.craigslist.org/%s/' % (city, catg)
      ROOT.append(r)

def lsSeen():
  global SEEN
  SEEN = set()
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        SEEN.add(postId(f))

def crawlRoot(r):
  log('> CRAWL ROOT %s' % r)
  cmd('wget --output-document=root.html --no-verbose %s' % r)

  sp = getSoup('root.html')
  log('>> PRETTY ROOT HTML')
  log(sp.prettify())

  ps = posts(sp)
  log('>> POSTS (%d)' % len(ps))
  log('\n'.join(ps))

  nps = newPosts(ps)
  log('>> NEW POSTS (%d)' % len(nps))
  log('\n'.join(nps))

  # todo send warning email if len(nps) > 100

  log('>> FETCHING NEW POSTS')
  for p in nps:
    cmd('wget --force-directories --no-verbose %s' % str(p))

  cmd('rm root.html')
  log('> FINISH ROOT %s' % r)

def getSoup(html):
  f = open(html, 'r')
  s = f.read()
  f.close()
  return BeautifulSoup(s)

def posts(soup):
  POST = '^http://.*\.craigslist\.org/.*/[0-9]*\.html$'
  ps = []
  for tag in soup.findAll('a', href=True):
    if re.match(POST, tag['href']):
      ps.append(tag['href'])
  return ps

def newPosts(ps):
  nps = []
  for p in ps:
    if postId(p) not in SEEN:
      nps.append(p)
  return nps

def postId(p):
  return p[-15:-5]

main()

