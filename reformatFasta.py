#!/usr/bin/env python

import re
import sys
from subprocess import check_call

inFile=sys.argv[1]
outFile=inFile+'_reformatted'
header=""
seq=""
test=0
data=[]

with open(inFile,"r") as INPUT:
	fasta=INPUT.read().strip().split("\n")

for line in fasta:
	if(">" in line):
		if(test!=0):
			data.append(header)
			data.append(seq)
		header=line
		seq=""
		test=1
	else:
		seq+=line
data.append(header)
data.append(seq)

for i in range(len(data)):
	if('>' in data[i]):
		if('>gene' in data[i]):
			g=re.search('(>gene_\d+).*',data[i])
			data[i]=">"+inFile+"_"+g.group(1)[1:]
		else:
			temp=data[i].split(" ")
			temp2=temp[8].split(";")
			m=re.search("ID=(\d+_\d+)",temp2[0])
			data[i]=">"+inFile+"_"+"prodigal_"+m.group(1)

with open(outFile,"w+") as OUTPUT:
	OUTPUT.write("\n".join(data))
	OUTPUT.write("\n")

check_call(["sed","-i","s/\.f[na]a//g",outFile])

if(".faa" in inFile):
	check_call(["sed","-ir","s/\*$//g",outFile])
