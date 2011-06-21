#!/usr/bin/env python

import re, sys, os, os.path, shlex, subprocess
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

def main():
  os.chdir('/home/ztatlock/cloth')
  init()
  for r in ROOT:
    crawlRoot(r)

def init():
  global SEEN
  SEEN = []
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        SEEN.append(postId(f))
  SEEN.sort()

def crawlRoot(r):
  cmd('wget --output-document=root.html --no-verbose %s' % r)
  sp = getSoup('root.html')
  ps = posts(sp)
  ps = newPosts(ps)
  for p in ps:
    cmd('wget --force-directories --no-verbose %s' % str(p))
  cmd('rm root.html')

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
  r = subprocess.call(shlex.split(c))
  if r != 0:
    print 'Warning: command failed!\n\t%s' % c

main()

#import cProfile
#cProfile.run('main()')

