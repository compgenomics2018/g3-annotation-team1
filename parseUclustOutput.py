#!/usr/bin/env python

import sys

inFile=sys.argv[1]
outFile1=sys.argv[2]
outFile2=sys.argv[3]
lengths={}
index={}

with open(inFile,"r") as INPUT:
	lines=INPUT.read().split("\n")

# loop 1 to find all the centroids and cluster sizes
for line in lines:
	temp=line.split("\t")
	if(temp[0]=="S"):
		index[temp[8]]=[]
		lengths[temp[8]]=1

# loop 2 to find cluster members (not the centroid)
for line in lines:
	temp=line.split("\t")
	if(temp[0]=="H"):
		index[temp[9]].append(temp[8])
		lengths[temp[9]]+=1

sortedCentroids = sorted(lengths, key=lambda x: lengths[x], reverse=True )

with open(outFile1,"w") as OUTPUT:
	for i in sortedCentroids:
		OUTPUT.write(i)
		for j in index[i]:
			OUTPUT.write("\t"+j)
		OUTPUT.write("\n")

with open(outFile2,"w") as OUTPUT:
	for i in sortedCentroids:
		OUTPUT.write(i+"\t"+str(lengths[i])+"\n")
