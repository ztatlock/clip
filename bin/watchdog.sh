#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
CLIP="$ROOT/bin/clipper.py"
DATA="$ROOT/data"

mkdir -p $DATA
mkdir -p $DATA/log

function running {
  ps ax \
    | grep $CLIP \
    | grep -v grep \
    &> /dev/null
}

function start {
  cd $DATA
  # capture any error output
  l="watchdog-$(date "+%y%m%d-%H%M%S").txt"
  $CLIP &> $DATA/log/$l &
}

if ! running; then
  start
fi
date > $DATA/log/last-watchdog-run.txt
