#!/usr/bin/env bash

cd /home/ztatlock/cloth/scrapes/

for r in $(cat ../roots.txt); do
  echo ">>> $r"
  ../crawl.py $r
done
