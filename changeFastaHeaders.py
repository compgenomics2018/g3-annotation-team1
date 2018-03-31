#!/usr/bin/env python

import sys
from subprocess import check_call

inFile=sys.argv[1]
outFile=inFile+".reformatted"

with open(outFile,"w+") as OUTPUT:
	with open(inFile,"r") as INPUT:
		for line in INPUT:
			if (">" in line):
				OUTPUT.write(">"+inFile+"_"+line[1:])
			else:
				OUTPUT.write(line)

check_call(["sed","-i","s/\.f[na]a//g",outFile])
