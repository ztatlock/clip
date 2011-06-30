#!/usr/bin/env python

import os, os.path, sys, re, time

FIELDS = 'city catg post date year month day hour minute ampm tzone tfhour dow'

def main():
  ps = []
  for p in lsPosts():
    p = Post(p)
    p.parsePath()
    p.parsePost()
    if p.deleted:
      continue
    p.extras()
    ps.append(p)
  writeCsv(ps)
  writeJson(ps)

def lsPosts():
  posts = []  
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if 'craigslist' in root and f.endswith('.html'):
        posts.append(os.path.join(root, f))
  posts.sort()
  return posts

def writeCsv(posts):
  f = open('posts.csv', 'w')
  f.write('%s\n' % FIELDS.replace(' ', ', '))
  for p in posts:
    f.write(p.csv() + '\n')
  f.close()

def writeJson(posts):
  f = open('posts.js', 'w')
  f.write('POSTS = [')
  first = True
  for p in posts:
    if first:
      first = False
    else:
      f.write(',')
    f.write(p.json())
  f.write('];')
  f.close()

class Post:
  def __init__(self, path):
    self.path = path

  def parsePath(self):
    #           city                      area      catg        post
    POST = '^.*/([a-z]*)\.craigslist\.org/([a-z]*/)?([a-z0-9]*)/([0-9]*)\.html$'
    m = re.match(POST, self.path)
    if m != None:
      self.city = m.group(1)
      self.catg = m.group(3)
      self.post = m.group(4)
    else:
      warn('failed to parse path %s' % self.path)
      self.deleted = True

  def parsePost(self):
    f = open(self.path, 'r')
    p = f.read()
    f.close()
    # has this post been removed?
    self.deleted = False
    DELT = 'This posting has (expired|been flagged for removal|been deleted by its author)\.'
    if re.search(DELT, p) != None:
      warn('no content in %s' % self.path)
      self.deleted = True
      return
    # extract date and time
    #             year       month      day         hour        min       ampm    tzone
    DTTM = 'Date: ([0-9]{4})-([0-9]{2})-([0-9]{2}), ([ 1][0-9]):([0-9]{2})(AM|PM) ([A-Z]{3})'
    m = re.search(DTTM, p)
    if m != None:
      self.year   = m.group(1)
      self.month  = m.group(2)
      self.day    = m.group(3)
      self.hour   = m.group(4)
      self.minute = m.group(5)
      self.ampm   = m.group(6)
      self.tzone  = m.group(7)
    else:
      warn('no date/time in %s' % self.path)
      self.deleted = True
      return

  def extras(self):
    self.date = '%s%s%s' % (self.year, self.month, self.day)
    # day of week
    t = time.strptime(self.date, '%Y%m%d')
    self.dow = time.strftime('%a', t)
    # twenty four hour hour
    if self.ampm == "PM" and self.hour < 12:
      self.tfhour = str(12 + int(self.hour))
    else:
      self.tfhour = self.hour

  def vals(self):
    vs = []
    for f in FIELDS.split():
      vs.append(eval('self.%s' % f))
    return vs

  def csv(self):
    return ', '.join(self.vals())

  def json(self):
    return '''
{ path   = "%s"
, city   = "%s"
, catg   = "%s"
, post   = "%s"
, date   = %s
, year   = %s
, month  = %s
, day    = %s
, hour   = %s
, minute = %s
, ampm   = "%s"
, tzone  = "%s"
, tfhour = %s
, dow    = "%s"
}
''' % ( self.path
      , self.city
      , self.catg
      , self.post
      , self.date
      , self.year
      , self.month
      , self.day
      , self.hour
      , self.minute
      , self.ampm
      , self.tzone
      , self.tfhour
      , self.dow
      )

def warn(msg):
  sys.stdout.write('Warning: %s\n' % msg)

main()
