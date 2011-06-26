#!/usr/bin/env python

import re, sys, os, os.path, shlex, subprocess, time
from BeautifulSoup import BeautifulSoup

CITY = ['charlotte', 'denver', 'portland', 'tampa', 'minneapolis', 'stlouis']
CATG = ['cas', 'msr', 'm4m', 'm4w', 'w4m', 'w4w']
POST = '^http://.*\.craigslist\.org/.*/[0-9]*\.html$'

ROOT = None
SEEN = None
LOG  = None

def main():
  init()
  for r in ROOT:
    crawlRoot(r)
  fin()

def init():
  global ROOT, SEEN, LOG
  # compute roots
  ROOT = []
  for city in CITY:
    for catg in CATG:
      r = 'http://%s.craigslist.org/%s/' % (city, catg)
      ROOT.append(r)
  # determine already seen posts
  SEEN = set()
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        SEEN.add(postId(f))
  # set up log
  if not os.path.isdir('log'):
    os.mkdir('log')
  i = 0
  l = 'log/crawl-%04d.txt' % i
  while os.path.exists(l):
    i += 1
    l = 'log/crawl-%04d.txt' % i
  # LOG must be unbuffered
  LOG = open(l, 'w', 0)
  log('BEGIN : %s' % now())

def fin():
  log('\n\nEND : %s' % now())
  LOG.close()

def crawlRoot(r):
  log('\n\n>>> CRAWL ROOT %s' % r)
  cmd('wget --output-document=root.html --no-verbose %s' % r)

  sp = getSoup('root.html')
  log('\n>> PRETTY ROOT HTML')
  log(sp.prettify())

  ps = posts(sp)
  log('\n>> POSTS (%d)' % len(ps))
  log('\n'.join(ps))

  nps = newPosts(ps)
  log('\n>> NEW POSTS (%d)' % len(nps))
  log('\n'.join(nps))

  # todo send warning email if len(nps) > 100

  log('\n>> FETCHING NEW POSTS')
  for p in nps:
    cmd('wget --force-directories --no-verbose %s' % str(p))

  cmd('rm root.html')
  log('\n>>> FINISHED ROOT %s' % r)

def getSoup(html):
  f = open(html, 'r')
  s = f.read()
  f.close()
  return BeautifulSoup(s)

def posts(soup):
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

def cmd(c):
  r = subprocess.call(shlex.split(c), stdout=LOG, stderr=LOG)
  if r != 0:
    print 'Warning: command failed!\n\t%s' % c

def log(msg):
  LOG.write(msg + '\n')

def now():
  return time.strftime('%A, %B %d, %Y at %I:%M:%S %p')

main()

#import cProfile
#cProfile.run('main()')

