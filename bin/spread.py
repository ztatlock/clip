#!/usr/bin/env python

import os, os.path, re, time

FIELDS = 'city catg post year month day hour minute ampm tzone'
LOG    = None

def main():
  init()
  ps = []
  for p in lsPosts():
    p = Post(p)
    p.parsePath()
    p.parsePost()
    if not p.deleted:
      ps.append(p)
  writeCsv(ps)
  fin()

def init():
  global LOG
  # set up log
  if not os.path.isdir('log'):
    os.mkdir('log')
  i = 0
  l = 'log/spread-%04d.txt' % i
  while os.path.exists(l):
    i += 1
    l = 'log/spread-%04d.txt' % i
  # LOG must be unbuffered
  LOG = open(l, 'w', 0)
  log('BEGIN : %s' % now())

def fin():
  log('\n\nEND : %s' % now())
  LOG.close()

def lsPosts():
  posts = []  
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if f.endswith('.html'):
        posts.append(os.path.join(root, f))
  posts.sort()
  return posts

def writeCsv(posts):
  f = open('posts.csv', 'w')
  f.write('%s\n' % FIELDS.replace(' ', ', '))
  for p in posts:
    f.write(p.csv() + '\n')
  f.close()

class Post:
  def __init__(self, path):
    self.path = path

  def parsePath(self):
    #           city                      area      catg        post
    POST = '^.*/([a-z]*)\.craigslist\.org/([a-z]*/)?([a-z0-9]*)/([0-9]*)\.html$'
    m = re.match(POST, self.path)
    if m:
      self.city = m.group(1)
      self.catg = m.group(3)
      self.post = m.group(4)
    else:
      warn('parsePath, match failed on "%s"' % self.path)

  def parsePost(self):
    f = open(self.path, 'r')
    p = f.read()
    f.close()
    # has this post been removed?
    self.deleted = False
    DELT = 'This posting has (expired|been flagged for removal|been deleted by its author)\.'
    if re.search(DELT, p):
      self.deleted = True
      return
    # extract date and time
    #             year       month      day         hour        min       ampm    zone
    DTTM = 'Date: ([0-9]{4})-([0-9]{2})-([0-9]{2}), ([ 1][0-9]):([0-9]{2})(AM|PM) ([A-Z]{3})'
    m = re.search(DTTM, p)
    if m:
      self.year   = m.group(1)
      self.month  = m.group(2)
      self.day    = m.group(3)
      self.hour   = m.group(4)
      self.minute = m.group(5)
      self.ampm   = m.group(6)
      self.tzone  = m.group(7)
    else:
      warn('parsePost, date/time search failed in "%s"' % self.path)

  def vals(self):
    vs = []
    for f in FIELDS.split():
      vs.append(eval('self.%s' % f))
    return vs

  def csv(self):
    return ', '.join(self.vals())

def now():
  return time.strftime('%A, %B %d, %Y at %I:%M:%S %p')

def log(msg):
  LOG.write(msg + '\n')

def warn(msg):
  LOG.write('Warning: %s\n' % msg)

main()

#import cProfile
#cProfile.run('main()')

