#!/bin/bash

cd /home/guest/processing/execfp

while [ 1 ]
do
	while [ 1 ]
	do
		day=`date +%d`
		minute=`date +%M`
		hour=`date +%H`
		second=`date +%S`
		if [ "$second" == "10" ]; then
			#echo "Clean hashes of database"
			/bin/bash /home/guest/processing/execfp/exec_hashe_server.sh
		fi

		if [ "$second" == "12" ]; then
			python /home/guest/processing/execfp/execfp_clean_databases_cubie.py $minute  >> /dev/null 2>&1 &
		fi

		if [ "$second" == "55" ]; then
			source /var/www/openpeople/setting.txt
			if [ "$permit" == "nao" ]
			then
				echo "$hour:$minute:$second - System is locked" >> /tmp/permit.log
				sleep 1
				continue
			fi
			break
		fi
		sleep 0.5
	done

	/bin/bash /home/guest/processing/execfp/loop_identify.sh $minute $hour $day &
	sleep 7
done
