#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
PATH="$ROOT/bin:$PATH"
DATA="$ROOT/data"

function main {
  cd $DATA
  spread.py
}

main >> $DATA/log/daily_$(date "+%y-%m-%d_%H-%M-%S").txt 2>&1

