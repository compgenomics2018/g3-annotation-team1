#!/usr/bin/env python

import sys
import re

mergedFile=sys.argv[1]
clusterFile=sys.argv[2]
outFile=clusterFile+".fasta"
data={}

with open(mergedFile,"r") as SOURCE:
	info=SOURCE.read().strip().split("\n")

headers=info[::2]
sequences=info[1::2]
del info

for i in range(len(headers)):
	m=re.search(">(SRR\d+)_(.*)",headers[i])
	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			print("This is wrong")
		data[m.group(1)][m.group(2)]=sequences[i]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]=sequences[i]

with open(clusterFile,"r") as INPUT:
	lines=INPUT.read().strip().split("\n")

with open(outFile,"w+") as OUTPUT:
	for line in lines:
		n=re.search(">(SRR\d+)_(.*)",line)
		OUTPUT.write(line+"\n"+data[n.group(1)][n.group(2)]+"\n")
