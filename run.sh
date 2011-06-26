#!/usr/bin/env bash

CLOTH="/home/ztatlock/cloth"

cd $CLOTH/data
$CLOTH/bin/crawl.py
$CLOTH/bin/spread.py

