#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
os
'''
import os, sys, glob, datetime
import datetime

'''
db
'''
import MySQLdb

'''
dejavu
'''
from dejavu import Dejavu
from dejavu.h_recognize import HFileRecognizer
import dejavu.decoder as decoder

if len(sys.argv) != 5:
	
	print "Params: " + str(len(sys.argv)) +"  Try " + sys.argv[0] + " hashe_file   minute   hora"
	for p in range(len(sys.argv)):
		print "PARAM[%d]: %s" %(p, sys.argv[p])

	sys.exit(0)

minute=sys.argv[2]
hora=sys.argv[3]
day=sys.argv[4]
config = {"database": {"host": "192.168.0.100","user": "root","passwd": "userpasswd","db":  "peoplemeter" + minute,},"database_type" : "mysql","fingerprint_limit" : -1}
djv = Dejavu(config, "HOLD_TABLE")

hashe_name=sys.argv[1]
channel = None

channel = djv.recognize(HFileRecognizer, hashe_name)


date_hour   = datetime.datetime.now().strftime("%Y-%m-")
date_hour_z = date_hour

date_hour = date_hour + day + " "  + hora + ":" + minute + ":30"
date_hour_z = date_hour_z + day + " " + hora + ":" + minute + ":00"

cod_channel = None


if channel is not None:

	if   "ric" in channel["song_name"]:
		channel_name = "RECORD"
		cod_channel = "4"

	elif "rbs" in channel["song_name"]:
		channel_name = "GLOBO        " 
		cod_channel = "12"

	elif "band" in channel["song_name"]:
		channel_name = "BAND    "
		cod_channel = "9"

	elif "kids" in channel["song_name"]:
		channel_name = "DISCOVERY KIDS" 
		cod_channel = "100"

	elif "rnews" in channel["song_name"]:
		channel_name = "RECORD NEWS   " 
		cod_channel = "6"

	elif "redetv" in channel["song_name"]:
		channel_name = "REDE TV       " 
		cod_channel = "21"

	elif "sbt" in channel["song_name"]:
		channel_name = "SBT        " 
		cod_channel = "45"

	elif "tval" in channel["song_name"]:
		channel_name = "TV AL         " 
		cod_channel = "16"

	elif "sportv1" in channel["song_name"]:
		channel_name = "SPORTV1         " 
		cod_channel = "39"

	elif "sportv2" in channel["song_name"]:
		channel_name = "SPORTV2         " 
		cod_channel = "38"

	elif "gnews" in channel["song_name"]:
		channel_name = "GNEWS         " 
		cod_channel = "40"

	elif "viva" in channel["song_name"]:
		channel_name = "VIVA         " 
		cod_channel = "43"

	elif "universal" in channel["song_name"]:
		channel_name = "UNIVERSAL         " 
		cod_channel = "130"

	elif "cultura" in channel["song_name"]:
		channel_name = "CULTURA         " 
		cod_channel = "7"

	elif "foxsports1" in channel["song_name"]:
		channel_name = "FOXSPORTS       " 
		cod_channel = "73"

	elif "foxsports2"  in channel["song_name"]:
		channel_name = "FOXSPORTS       " 
		cod_channel = "74"

	elif "cartoon" in channel["song_name"]:
		channel_name = "CARTOON       " 
		cod_channel = "104"

	elif "space" in channel["song_name"]:
		channel_name = "SPACE        " 
		cod_channel = "154"

	elif "espn" in channel["song_name"]:
		channel_name = "ESPN        " 
		cod_channel = "70"

	elif "tcpremium" in channel["song_name"]:
		channel_name = "TCPREMIUN        " 
		cod_channel = "161"

	elif "megapix" in channel["song_name"]:
		channel_name = "MEGAPIX        " 
		cod_channel = "152"

	elif "disneych" in channel["song_name"]:
		channel_name = "DISNEY CH " 
		cod_channel = "102"

	elif "disneyxd" in channel["song_name"]:
		channel_name = "DISNEY XD " 
		cod_channel = "105"

	elif "multshow" in channel["song_name"]:
		channel_name = "MULTSHOW " 
		cod_channel = "42"

	elif "foxfilmes" in channel["song_name"]:
		channel_name = "FOX       " 
		cod_channel = "131"

	elif "dischhome" in channel["song_name"]:
		channel_name = "DISCH HOME       " 
		cod_channel = "55"

	elif "discchannel" in channel["song_name"]:
		channel_name = "DISCH CHANNEL      " 
		cod_channel = "81"

	elif "warner" in channel["song_name"]:
		channel_name = "WARNER       " 
		cod_channel = "132"

	elif "nickodeon" in channel["song_name"]:
		channel_name = "NICKODEON       " 
		cod_channel = "103"

	else:
		channel_name = "OTHER - Unmonitored"
		cod_channel = "4097"

else:
	cod_channel = "4097"
	channel_name = "OTHER      "

con = None

try:
	cod_base_station = hashe_name.split("_")[1]

	#----------------------
	mysql_con = MySQLdb.connect('192.168.0.100', 'root', 'userpasswd')
	mysql_con.select_db('last_chan')
	mysql_cursor = mysql_con.cursor()

	mysql_cursor.execute("SELECT * FROM register WHERE `peoplemeter` = '%s'" % cod_base_station)
	rows = mysql_cursor.fetchone()
	if rows is None:
		mysql_cursor.execute("INSERT INTO `register` (`peoplemeter`, `canal`) VALUES ('%s', '%s')" % (cod_base_station, cod_channel))
	else:
		# This base station already in other channel
		if int(rows[1]) == 4097:
			# Identify channl in the lista, was not possible, then it is other.
			if cod_channel == "4097":
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `canal` = '%s' WHERE  `register`.`peoplemeter` =%s" % (cod_channel, cod_base_station))
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `hora` = '%s' WHERE  `register`.`peoplemeter` =%s" % (date_hour, cod_base_station))
			else:
                                # Channel identified
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `canal` = '%s' WHERE  `register`.`peoplemeter` =%s" % (cod_channel, cod_base_station))
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `hora` = '%s' WHERE  `register`.`peoplemeter` =%s" % (date_hour, cod_base_station))
		else:
                        # base station is knew
			if cod_channel == "4097":
                                # Repeat channel, and wait if next channel is other. Debounce work around
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `canal` = '%s' WHERE `register`.`peoplemeter` =%s" % (cod_channel, cod_base_station))
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `hora` = '%s' WHERE `register`.`peoplemeter` =%s" % (date_hour, cod_base_station))
				cod_channel = str(rows[1])
			else:
                                # Ideal situation. channel identified
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `canal` = '%s' WHERE `register`.`peoplemeter` =%s" % (cod_channel, cod_base_station))
				mysql_cursor.execute("UPDATE `last_chan`.`register` SET `hora` = '%s' WHERE `register`.`peoplemeter` =%s" % (date_hour, cod_base_station))

	mysql_con.commit()
	mysql_con.close()

except:
	print "erro"



try:
	report_conn = None
	report_conn = MySQLdb.connect('192.168.0.101', 'root', 'userpasswd', 'peoplemeter_base')

	report_cur = report_conn.cursor()

	query  = "INSERT INTO peoplemeter_monitor (cod_peopletv_aparelho, cod_peopletv_canal, dta_data, dta_data_partition) "
	query += "VALUE (\"" + cod_base_station + "\", \"" + cod_channel + "\", \"" + date_hour_z + "\", TO_DAYS(DATE(\"" + date_hour_z +"\")))"

	report_cur.execute(query)
	report_conn.commit()
	print str(datetime.datetime.now()) + " - ASSIN:" + cod_base_station + " - COD:"+ cod_channel + " - HOUR:" + date_hour_z

	if report_conn:
            report_conn.close()
except:
	print "********* Fail to connect to MySQLReports **************"
