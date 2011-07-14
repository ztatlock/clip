#!/usr/bin/env python

import config, time
from boomslang import *

class Post:
  def __init__(self, city, catg, year, month, day, hour, min):
    t = '%s%s%s%s%s' % (year, month, day, hour, min)
    t = time.strptime(t, '%Y%m%d%H%M')
    self.city = city
    self.catg = catg
    self.t    = t
    self.dow  = time.strftime('%a', t)
    self.doy  = int(time.strftime('%j', t))

POSTS = []
csv = open('../data/posts.csv')
first = True
for l in csv:
  if first:
    first = False
    continue
  l = l.strip()
  l = l.split(',')
  # can remove this once tfhour fix is in
  h = '%02d' % int(l[10])
  p = Post(l[0], l[1], l[3], l[4], l[5], h, l[7])
  POSTS.append(p)
csv.close()

DAYS = range(173, 215)

by_doy = {}
for d in DAYS:
  by_doy[d] = []
for p in POSTS:
  if p.doy in DAYS:
    by_doy[p.doy].append(p)

def bwPlot():
  p = Plot()
  p.addLineColor('black')
  p.addLineColor('gray')
  p.addLineStyle('-')
  p.addLineStyle('--')
  p.addLineStyle(':')
  return p

def lbl(x):
  return { 'denver'      : 'Denver'
         , 'minneapolis' : 'Minneapolis'
         , 'portland'    : 'Portland'
         , 'tampa'       : 'Tampa'
         , 'stlouis'     : 'St. Louis'
         , 'charlotte'   : 'Charlotte'
         , 'cas'         : 'cas'
         , 'm4m'         : 'm4m'
         , 'm4w'         : 'm4w'
         , 'w4m'         : 'w4m'
         , 'w4w'         : 'w4w'
         , 'msr'         : 'msr'
         }[x]

def doy_line(test, label=None):
  ys = []
  for d in DAYS:
    ps = by_doy[d]
    ps = filter(test, ps)
    ys.append(len(ps))
  line = Line()
  line.xValues = DAYS
  line.yValues = ys
  if label != None:
    line.label = label
  return line

plot = bwPlot()
l = doy_line(lambda p: True)
plot.add(l)
plot.setXLabel('Day of Year')
plot.setYLabel('Total Posts')
plot.setTitle('Total Posts Across All Cities and Categories')
plot.save('global.png')

plot = bwPlot()
for cy in config.cities:
  l = doy_line(lambda p: p.city == cy, lbl(cy))
  plot.add(l)
plot.setXLabel('Day of Year')
plot.setYLabel('Total Posts')
plot.setTitle('Total Posts by City')
plot.hasLegend()
plot.save('bycity-all.png')

plot = bwPlot()
for cg in config.catgs:
  l = doy_line(lambda p: p.catg == cg, lbl(cg))
  plot.add(l)
plot.setXLabel('Day of Year')
plot.setYLabel('Total Posts')
plot.setTitle('Total Posts by Category')
plot.hasLegend()
plot.save('bycatg-all.png')

YMAX = 1250

for cg in config.catgs:
  plot = bwPlot()
  for cy in config.cities:
    l = doy_line(lambda p: p.city == cy and p.catg == cg, lbl(cy))
    plot.add(l)
  plot.setXLabel('Day of Year')
  plot.setYLabel('Total Posts in %s' % lbl(cg))
  plot.setTitle('Total Posts by City for %s' % lbl(cg))
  plot.setYLimits(0, YMAX)
  plot.hasLegend()
  plot.save('bycity-%s.png' % cg)

for cy in config.cities:
  plot = bwPlot()
  for cg in config.catgs:
    l = doy_line(lambda p: p.city == cy and p.catg == cg, lbl(cg))
    plot.add(l)
  plot.setXLabel('Day of Year')
  plot.setYLabel('Total Posts in %s' % lbl(cy))
  plot.setTitle('Total Posts by Category in %s' % lbl(cy))
  plot.setYLimits(0, YMAX)
  plot.hasLegend()
  plot.save('bycatg-%s.png' % cy)

