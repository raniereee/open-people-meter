#!/bin/bash
# Exec: ./audio_capture_process.sh > sox.log 2>&1 &

mkdir /tmp/audios
cd /home/guest/capture

DIRECTORY_TO_FINGERPRINT="/tmp/audios"
TOTAL_OF_CHANNELS=1

source /etc/open-people-meter/confs.txt

rm /tmp/audios/*.wav

while [ 1 ]; do
	#Check if 0 second
	while [ 1 ]; do
		second=`date +%S`
		if [ "$second" == "02" ]; then
			echo "System init second 02."
			break
		fi

		echo "Stoped in second: "$second

		sleep 0.6
	done

	minute=`date +%M`

	dir="/tmp/audios"
	audio_file="/tmp/audios/"$canal"20.wav"
	audio_file2="/tmp/audios/"$canal"21.wav"
	t=`rm -rf $audio_file $audio_file2`

	# Record of sound card
	sox -v 0.80 -r 44100 -c 1 -d $audio_file  trim 0 00:15  >> /dev/null 2>&1
	sox -v 0.80 -r 44100 -c 1 -d $audio_file2 trim 0 00:15  >> /dev/null 2>&1

	second=`date +%S`
	hora=`date +%H`

	echo "== Start fploop ==="
	python execfp.py $dir $minute &

done
