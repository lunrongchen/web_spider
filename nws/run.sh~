#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

while true; do
    cd $DIR/daily/
    scrapy crawl baidu
    plsql-d news2 -c "update process set lock=false where id=1;"
    cd $DIR/parsePage
    python process.py
    cd $DIR/filter
    python filter.py
    sleep 5m
done

