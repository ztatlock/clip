#!/usr/bin/env bash

ROOT="/home/ztatlock/clip"
PATH="$ROOT/bin:$PATH"
DATA="$ROOT/data"

function main {
  cd $DATA
  parser.py
  cp ../www/* .
  rsync -r $DATA/ godel:/var/www/cldata/
}

l="analysis-$(date "+%y%m%d-%H%M%S").txt"
main &> $DATA/log/$l
