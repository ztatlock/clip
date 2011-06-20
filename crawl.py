#!/usr/bin/env python

import re
import sys
import shlex
import subprocess
from BeautifulSoup import BeautifulSoup

ROOT = sys.argv[1]

POST_PAT = 'http://.*\.craigslist\.org/.*/[0-9]*\.html'

def main():
  # fetch ROOT
  cmd('wget -O root.html %s' % ROOT)

  # get contents of root.html 
  f = open('root.html', 'r')
  html = f.read()
  f.close()

  posts = extract_posts(html)
  for post in posts:
    cmd('wget --force-directories %s' % str(post))

def extract_posts(html):
  links = extract_links(html)
  posts = []
  for link in links:
    if re.match(POST_PAT, link):
      posts.append(link)
  return posts

def extract_links(html):
  soup = BeautifulSoup(html)
  links = []
  for tag in soup.findAll('a', href=True):
    links.append(tag['href'])
  return links

def cmd(c):
  r = subprocess.call(shlex.split(c))
  if r != 0:
    print 'Warning: wget failed!'

main()

# ---

# Anne's wget program!
#
# import sys
# import urllib
#
# url = sys.argv[1]
#
# f = urllib.urlopen(url)
# ls = f.readlines()
# f.close()
#
# for l in ls:
#     print l,
#
