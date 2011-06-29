#!/usr/bin/env bash

ROOT="/home/ztatlock/cloth"
PATH="$ROOT/bin:$PATH"
DATA="$ROOT/data"

function main {
  cd $DATA
  spread.py
}

main >> $DATA/daily_$(date "+%y-%m-%d_%H-%M-%S")_log.txt 2>&1

