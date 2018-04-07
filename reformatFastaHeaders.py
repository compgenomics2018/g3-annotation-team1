#!/usr/bin/env python

import re
import sys

inFile=sys.argv[1]
outFile=inFile+'_reformatted'

with open(inFile,"r") as INPUT:
	data=INPUT.read().strip().split("\n")

for i in range(len(data)):
	if('>' in data[i]):
		if('>gene' in data[i]):
			g=re.search('(>gene_\d+).*',data[i])
			data[i]=g.group(1)
		else:
			temp=data[i].split(" ")
			temp2=temp[8].split(";")
			m=re.search("ID=(\d+_\d+)",temp2[0])
			data[i]=">prodigal_"+m.group(1)

with open(outFile,"w+") as OUTPUT:
	OUTPUT.write("\n".join(data))
