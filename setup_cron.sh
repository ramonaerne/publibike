#!/bin/bash

# setup directories
mkdir -p data
mkdir -p logs

# setup crontab
CWD="$(pwd)"
NUM_CRONTABS="$(crontab -l | sed 's/^ *//;/^[*@0-9]/!d' | wc -l)"

if [ ${NUM_CRONTABS} -lt 1 ]; then
	echo "*/5 * * * * python3 ${CWD}/crawl_once.py >> ${CWD}/logs/cron_output.log 2>&1" > mycron
	crontab mycron
	rm mycron
else
	echo "crontabs already running, don't create one"
fi
