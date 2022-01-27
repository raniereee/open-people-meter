#!/bin/bash
# ./rec_audio_60s.sh > sox.log 2>&1 &

HASHES_DIR="/home/guest/capture/hashes_server/hashes"

cd /home/guest/processing/execfp

minute=$1
hour=$2
day=$3

contador=0
while [ 1 ]
do
	cmd_list_hashes=$HASHES_DIR"/"$minute"/*.tar.gz"
	hashes_compress=`ls $cmd_list_hashes 2> /dev/null`

	# Here, process of identify of each file of hash came from 
	# base_station for minute now
	if [ -n "$hashes_compress" ]; then 
		t=`ls  -ltr $HASHES_DIR"/"$minute | wc -l`
		t=$(( $t - 1 ))
		echo "$hour:$minute - Total file on directory: $t"
	fi

	for file in $hashes_compress
	do
		contador=$(( $contador + 1 ))
		./identify_cubie.sh $file $minute $hour $day &
	done

	minute_now=`date +%M`

	if [ $minute_now -ge $minute ];
	then
		delta=$(( 10#$minute_now - 10#$minute ))
	else
		aux="60"
		delta=$(( 10#$minute_now + 10#$aux - 10#$minute ))
	fi

	# Waiting until 2 minutes to arrive all hashes files
	if [ $delta -gt "01" ];
	then
		echo "$hour:$minute - Hour of exit - Processeds: $contador"
		rm $HASHES_DIR"/"$minute"/*.tar.gz"
		break
	fi

	sleep 6
done
