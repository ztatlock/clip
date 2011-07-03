#!/usr/bin/env python

import config, os, os.path, sys, re, time

COLS = [ 'city'
       , 'catg'
       , 'post'
       , 'year'
       , 'month'
       , 'day'
       , 'hour'
       , 'min'
       , 'ampm'
       , 'tzone'
       , 'tfhour'
       , 't'
       , 'd'
       , 'dow'
       ]

def main():
  ps = []
  for p in lsPosts():
    p = Post(p)
    p.parsePath()
    if p.skip \
    or p.city not in config.cities \
    or p.catg not in config.catgs:
      continue
    p.parsePost()
    if p.skip:
      continue
    p.extras()
    ps.append(p)
  writeCsv(ps)
  writeJson(ps)

def lsPosts():
  ps = []
  for (root, dirs, files) in os.walk('.'):
    for f in files:
      if 'craigslist' in root and f.endswith('.html'):
        ps.append(os.path.join(root, f))
  return ps

def writeCsv(posts):
  f = open('posts.csv', 'w')
  f.write(','.join(COLS) + '\n')
  for p in posts:
    f.write(p.csv() + '\n')
  f.close()

def writeJson(posts):
  f = open('posts.js', 'w')
  f.write('POSTS = [\n')
  first = True
  for p in posts:
    if first:
      first = False
    else:
      f.write(',\n')
    f.write(p.json())
  f.write('];\n')
  f.close()

class Post:
  def __init__(self, path):
    self.path = path
    self.skip = False # used to signal anomaly

  def parsePath(self):
    #           city                      area        catg          post
    POST = '^.*/([a-z]*)\.craigslist\.org/([a-z]{3}/)?([a-z0-9]{3})/([0-9]{10})\.html$'
    m = re.match(POST, self.path)
    if m != None:
      self.city = m.group(1)
      self.catg = m.group(3)
      self.post = m.group(4)
    else:
      warn('failed to parse path %s' % self.path)
      self.skip = True

  def parsePost(self):
    f = open(self.path, 'r')
    p = f.read()
    f.close()
    DLET = 'This posting has (expired|been flagged for removal|been deleted by its author)\.'
    if re.search(DLET, p) != None:
      info('no content in %s' % self.path)
      self.skip = True
      return
    # extract date and time
    #             year       month      day         hour        min       ampm    tzone
    DTTM = 'Date: ([0-9]{4})-([0-9]{2})-([0-9]{2}), ([ 1][0-9]):([0-9]{2})(AM|PM) ([A-Z]{3})'
    m = re.search(DTTM, p)
    if m != None:
      self.year  = m.group(1)
      self.month = m.group(2)
      self.day   = m.group(3)
      self.hour  = m.group(4).strip() # may have a leading space
      self.min   = m.group(5)
      self.ampm  = m.group(6)
      self.tzone = m.group(7)
    else:
      warn('no date/time in %s' % self.path)
      self.skip = True
      return

  def extras(self):
    # twenty four hour hour
    h = int(self.hour)
    if self.ampm == 'AM':
      if h == 12: self.tfhour = str(0)
      else:       self.tfhour = str(h)
    else:
      if h == 12: self.tfhour = str(h)
      else:       self.tfhour = str(h + 12)
    # time, date all in one
    self.t = '%s%s%s%s%s' % (self.year, self.month, self.day, self.tfhour, self.min)
    self.d = '%s%s%s'     % (self.year, self.month, self.day)
    # day of week
    self.dow = time.strftime('%a', time.strptime(self.d, '%Y%m%d'))

  def proj(self, field):
    return eval('self.' + field)

  def projs(self, fs):
    return [self.proj(f) for f in fs]

  def nv_projs(self, fs):
    return [(f, self.proj(f)) for f in fs]

  def csv(self):
    return ','.join(self.projs(COLS))

  def json(self):
    nvs = self.nv_projs(['path'] + COLS)
    nvs = ['%s = "%s"' % nv for nv in nvs]
    return '{%s}' % ', '.join(nvs)

def warn(msg):
  sys.stderr.write('Warning: %s\n' % msg)

def info(msg):
  sys.stderr.write('HeadsUp: %s\n' % msg)

main()
