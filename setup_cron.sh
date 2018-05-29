#!/bin/bash

# setup directories
mkdir -p data
mkdir -p logs

# setup crontab
# it seems that the cronjobs get deleted at 0700 everyay
# therefore call this script from remote cron at 0701
# also make sure it is run from cronjob on this machine couple of times
# to make sure that it doesn't have too big gaps in case sth gets deleted
CWD=$(dirname -- "$(readlink -f "$0")")
NUM_CRONTABS="$(crontab -l 2> /dev/null | sed 's/^ *//;/^[*@0-9]/!d' | wc -l)"
if [ ${NUM_CRONTABS} -lt 1 ]; then
	echo "3 */3 * * * ${CWD}/setup_cron.sh" > mycron
	echo "*/5 * * * * python3 ${CWD}/crawl_once.py >> ${CWD}/logs/cron.log 2>&1" >> mycron
	crontab mycron
	rm mycron
fi
