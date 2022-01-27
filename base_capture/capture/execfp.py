#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dejavu import Dejavu
import dejavu.decoder as decoder

if len(sys.argv) != 3:
	print "Try " + sys.argv[0] + "directory_audio   minute"
	sys.exit()

directory=sys.argv[1]
minute=sys.argv[2]

config = {"database": {"host": "192.168.0.100","user": "userdb","passwd": ";passwdmysqldb;","db": "peoplemeter" + minute,},"database_type" : "mysql","fingerprint_limit" : -1}
djv = Dejavu(config, "HOLD_TABLE")

djv.fingerprint_directory(directory, [".wav"], 4)
