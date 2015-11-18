#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)

sudo apt-get install lighttpd
sudo ln -s $DIR/php_back/ /var/www/server
sudo apt-get install php5-pgsql


