#!/usr/bin/env bash

ROOT=$1
DATA=$ROOT/data
CLIP=$ROOT/bin/clipper.py

function running {
  ps aux \
    | grep $CLIP \
    | grep -v grep
}

function alarm {
  sendmail ztatlock@gmail.com <<EOF
Subject: HEADS UP! clipper not running

$(date)

Clipper was not running, so I started it.

EOF
}

function start {
  $CLIP --data $DATA \
        --cities charlotte denver portland tampa minneapolis stlouis \
        --catgs cas msr m4m m4w w4m w4w \
        --minWait 50 \
        --maxWait 60
}

if ! running; then
  alarm
  start
fi

