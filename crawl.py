#!/usr/bin/env python

import re, sys, os, os.path, shlex, subprocess, time
from BeautifulSoup import BeautifulSoup

ROOT = [ 'http://sandiego.craigslist.org/cas/'
       , 'http://sandiego.craigslist.org/msr/'
       , 'http://sandiego.craigslist.org/m4m/'
       , 'http://sandiego.craigslist.org/m4w/'
       , 'http://sandiego.craigslist.org/w4m/'
       , 'http://sandiego.craigslist.org/w4w/'
       , 'http://charlotte.craigslist.org/cas/'
       , 'http://charlotte.craigslist.org/msr/'
       , 'http://charlotte.craigslist.org/m4m/'
       , 'http://charlotte.craigslist.org/m4w/'
       , 'http://charlotte.craigslist.org/w4m/'
       , 'http://charlotte.craigslist.org/w4w/'
       , 'http://orlando.craigslist.org/cas/'
       , 'http://orlando.craigslist.org/msr/'
       , 'http://orlando.craigslist.org/m4m/'
       , 'http://orlando.craigslist.org/m4w/'
       , 'http://orlando.craigslist.org/w4m/'
       , 'http://orlando.craigslist.org/w4w/'
       ] 
POST = '^http://.*\.craigslist\.org/.*/[0-9]*\.html$'
SEEN = None
LOG  = None

def main():
  os.chdir('/home/ztatlock/cloth')
  init()
  for r in ROOT:
    crawlRoot(r)
  fin()

def init():
  global SEEN, LOG
  SEEN = []
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        SEEN.append(postId(f))
  SEEN.sort()
  if not os.path.isdir('log'):
    os.mkdir('log')
  i = 0
  l = 'log/log-%04d.txt' % i
  while os.path.exists(l):
    i += 1
    l = 'log/log-%04d.txt' % i
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
    if not (postId(p) in SEEN):
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

