#!/bin/bash

while true; do
    scrapy crawl sina2
    scrapy crawl renmin
    scrapy crawl xinhua2
    scrapy crawl huanqiu
    scrapy crawl ifeng
    scrapy crawl baidu
    python ../../contentFilter/preprocess/preprocess.py
    python ../../contentFilter/locationFilter/locationFilter.py
    sleep 20m
done

