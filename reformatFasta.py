#!/usr/bin/env python

import sys

inFile=sys.argv[1]
outFile=inFile+".reformatted"
test=0
header=""
seq=""

with open(outFile,"w+") as OUTPUT:
	with open(inFile,"r") as INPUT:
		for line in INPUT:
			if(test==0):
				if(">" in line):
					header=line
					seq=""
					test=1
			else:
				if (">" in line):
					OUTPUT.write(header+seq+"\n")
					header=line
					seq=""
					test=1
				else:
					seq+=line.strip()
	OUTPUT.write(header+seq+"\n")
