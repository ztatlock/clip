#!/usr/bin/env bash

CLOTH="/home/ztatlock/cloth"

cd $CLOTH/data

$CLOTH/bin/crawl.py \
  --city charlotte denver portland \
         tampa minneapolis stlouis \
  --catg cas msr m4m m4w w4m w4w   \
  --minWait 50 --maxWait 60

