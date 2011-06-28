
import os, os.path, shlex, subprocess, time

def openLog(nm):
  global LOG
  if not os.path.isdir('log'):
    os.mkdir('log')
  d = time.strftime('%y-%m-%d')
  t = time.strftime('%H-%M-%S')
  l = 'log/%s_%s_%s.txt' % (nm, d, t) 
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

