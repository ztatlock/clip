#!/usr/bin/env python

import re, random, time
import os, os.path, shlex, subprocess
from BeautifulSoup import BeautifulSoup

# which cities and categories to sample
CITY = 'charlotte denver portland tampa minneapolis stlouis'
CATG = 'cas msr m4m m4w w4m w4w'

# min and max minutes between samples
MINM = 45
MAXM = 60

def main():
  while True:
    t0 = time.time()
    crawl()
    t1 = time.time()
    s = random.randrange(MINM, MAXM+1) * 60
    s = s - (t1 - t0) # adjust for crawl time
    time.sleep(s)

def crawl():
  lsSeen()
  openLog()
  for cy in CITY.split():
    for cg in CATG.split():
      r = 'http://%s.craigslist.org/%s/' % (cy, cg)
      n = crawlRoot(r)
      if n >= 95:
        n = crawlRoot(r + 'index100.html')
      if n >= 95:
        n = crawlRoot(r + 'index200.html')
      if n >= 95:
        warn('probably missing some posts')
  closeLog()

def lsSeen():
  global SEEN
  SEEN = set()
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        SEEN.add(postId(f))

def crawlRoot(r):
  log('>>> begin crawling %s' % r)
  cmd('wget --output-document=root.html --no-verbose %s' % r)

  sp = getSoup('root.html')
  log('>>> pretty printed html')
  log(sp.prettify())

  ps = posts(sp)
  log('>>> all posts (%d)' % len(ps))
  log('\n'.join(ps))

  ps = newPosts(ps)
  log('>>> new posts (%d)' % len(ps))
  log('\n'.join(ps))

  log('>>> fetching new posts')
  for p in ps:
    cmd('wget --force-directories --no-verbose %s' % str(p))

  cmd('rm root.html')
  log('>>> end crawling %s' % r)
  return len(ps)

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

def openLog():
  global LOG
  l = time.strftime('log/clipper-%y%m%d-%H%M%S.txt')
  LOG = open(l, 'w', 0) # unbuffered
  log(now())

def closeLog():
  log(now())
  LOG.close()

def log(msg):
  LOG.write('\n%s\n' % msg)

def warn(msg):
  log('*** WARNING ***\n%s' % msg)

def now():
  return time.strftime('%A, %B %d, %Y at %I:%M:%S %p')

def cmd(c):
  r = subprocess.call(shlex.split(c), stdout=LOG, stderr=LOG)
  if r != 0:
    warn('command failed:\n\t%s' % c)

main()

