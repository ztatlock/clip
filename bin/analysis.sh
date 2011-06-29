#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
PATH="$ROOT/bin:$PATH"
DATA="$ROOT/data"

function main {
  cd $DATA
  parser.py
  cp ../www/* .
}

l="analysis-$(date "+%y%m%d-%H%M%S").txt"
main &> $DATA/log/$l
