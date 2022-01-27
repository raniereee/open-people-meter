#!/bin/bash

# Directory where hashes are saveds for webserver that receive 
# from base_stations
cd  /home/guest/processing/hashes_server

find . -name *.gz -exec rm {} +
find . -name *.tmp -exec rm {} +
