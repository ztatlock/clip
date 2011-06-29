#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
PATH="$ROOT/bin:$PATH"
DATA="$ROOT/data"

clipper.py \
  --data $DATA \
  --cities charlotte denver portland tampa minneapolis stlouis \
  --catgs cas msr m4m m4w w4m w4w \
  --minWait 50 \
  --maxWait 60 \
  >> $DATA/clipper-log.txt 2>&1
