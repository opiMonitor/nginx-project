#!/bin/sh
PATH=$PATH:/bin:/usr/bin:/bin/sh:/usr/local/bin
export PATH

cd /app/zabbix_hosts/hostspider  #prawidlowa sciezka
scrapy crawl hosts > /app/log/`date +\%m\%d\%H\%M`-log.txt 2>&1 #prawidlowa sciezka
