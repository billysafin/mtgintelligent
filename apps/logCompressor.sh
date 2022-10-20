#!/bin/sh

cd /var/www/apps/log/
DELDAY=`date --date '6 months ago' '+%Y%m%d'`

for i in $(ls -1t *.log | head -3); do
    FILEDATE=`echo "$i" | sed -e 's/[^0-9]//g'`
    if [ $DELDAY -gt $FILEDATE ] ; then
        rm -f $i
    else
        bzip2 -z -9 $i
    fi
done