#!/usr/bin/env bash

cd scrapes/

for r in $(cat ../roots.txt); do
  echo ">>> $r"
  ../crawl.py $r
done
