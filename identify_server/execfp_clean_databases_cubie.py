#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from dejavu import Dejavu
import dejavu.decoder as decoder

if len(sys.argv) != 2:
	print "Try " + sys.argv[0] + "directory_audio   minute"
	sys.exit()

minute=sys.argv[1]

config = {"database": {"host": "192.168.0.100","user": "root","passwd": "userpasswd","db": "peoplemeter" + minute,},"database_type" : "mysql","fingerprint_limit" : -1}
djv = Dejavu(config, "CLEAN_TABLE")
