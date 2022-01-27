#!/bin/bash
source /etc/basestation/serial_number.txt
cd /home/guest/app

# waiting for network
error_count=0
while [ 1 ]
do
	ret=`ping 8.8.8.8 -W 1 -c 2 | wc -l`
	if [ "$ret" == "7" ]; then
		d=`date`
		echo "$d - its ok: 8.8.8.8"
		break
	fi

	sleep 1
done

# application
python /home/guest/app/BaseStation.py $serial $cidade >> /dev/null
