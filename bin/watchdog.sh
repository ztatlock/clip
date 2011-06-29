#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
CLIP="$ROOT/bin/clipper.py"
DATA="$ROOT/data"

mkdir -p $DATA
mkdir -p $DATA/log

function running {
  ps ax \
    | grep $CLIP \
    | grep -v grep
}

function start {
  cd $DATA
  $CLIP >> $DATA/log/watchdog_$(date "+%y-%m-%d_%H-%M-%S").txt 2>&1 &
}

if ! running; then
  start
fi

