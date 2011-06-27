#!/usr/bin/env python

import argparse, os, re, random, time
from BeautifulSoup import BeautifulSoup
from common import *

def main():
  cl = parseCmdLn()
  rs = mkRoots(cl.city, cl.catg)
  while True:
    lsSeen()
    openLog('crawl')
    for r in rs:
      crawlRoot(r)
    closeLog()
    nap(cl.minWait, cl.maxWait)

def parseCmdLn():
  d = 'Sample craigslist posts from select cities in select categories.'
  clp = argparse.ArgumentParser(description = d)
  clp.add_argument( '--city'
                  , default = []
                  , nargs   = '+'
                  , metavar = 'CY'
                  , help    = 'which cities to sample from'
                  )
  clp.add_argument( '--catg'
                  , default = []
                  , nargs   = '+'
                  , metavar = 'CG'
                  , help    = 'which categories to sample from'
                  )
  clp.add_argument( '--minWait'
                  , metavar = 'm'
                  , default = 60
                  , type    = int
                  , help    = 'minimum minutes to wait between samples'
                  )
  clp.add_argument( '--maxWait'
                  , metavar = 'm'
                  , default = 60
                  , type    = int
                  , help    = 'maximum minutes to wait between samples'
                  )
  return clp.parse_args()

def mkRoots(city, catg):
  rs = []
  for cy in city:
    for cg in catg:
      r = 'http://%s.craigslist.org/%s/' % (cy, cg)
      rs.append(r)
  return rs

def nap(lo, hi):
  dur = random.randrange(lo, hi+1) * 60
  time.sleep(dur)

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

  if len(nps) >= 95:
    warn('MISSING SOME POSTS!')

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

