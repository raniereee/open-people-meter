#!/bin/bash

file=$1
minute=$2
hour=$3
day=$4

t=`echo "scale=6; $RANDOM/32767" | bc`
sleep $t

tar -xzf $file
f=`tar tvfz $file | awk '{print $6}'`
rm $file

hashe_size=`du -s $f | awk '{print $1}'`

if [ $hashe_size -le 4 ];
then
	d=`date +%Y-%m-`"$day"

	# In case of TV power off, hashe file is low.
	./tvoff $f "'$d $hour":"$minute":"00'"   "'$d $hour":"$minute":"00'"  >> /tmp/outfile_without_audio.log 2>&1
	rm -f $f
	exit
fi

python fpidentify_cubie.py $f $minute $hour $day   >> /tmp/outfile_with_audio.log 2>&1 

rm -f $f

