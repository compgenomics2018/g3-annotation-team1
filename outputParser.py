#!/usr/bin/env python

import re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-l", "--LipoP", action="store", type="string", dest="LipoP_File",
                  help="LipoP short output file")

parser.add_option("-d", "--deepArg", action="store", type="string", dest="deepArg_File",
                  help="deepArg output file")

parser.add_option("-e", "--eggnogDiamond", action="store", type="string", dest="eggnogDiamond_File",
                  help="eggnogDiamond annotations output file")

parser.add_option("-t", "--tmhmm", action="store", type="string", dest="tmhmm_File",
                  help="tmhmm short output file")

parser.add_option("-s", "--signalp", action="store", type="string", dest="signalp_File",
                  help="signalp short output file")

parser.add_option("-p", "--phobius", action="store", type="string", dest="phobius_File",
                  help="phobius short output file")

parser.add_option("-u", "--uclust", action="store", type="string", dest="uc_File",
                  help="uclust uc output file")

parser.add_option("-g", "--mergedgff", action="store", type="string", dest="gff_File",
                  help="merged gff file")

parser.add_option("-r", "--door2", action="store", type="string", dest="door2_File",
                  help="door2 output file")

parser.add_option("-c", "--card", action="store", type="string", dest="card_File",
                  help="card output file")

parser.add_option("-v", "--vfdb", action="store", type="string", dest="vfdb_File",
                  help="vfdb output file")

parser.add_option("-o", "--outdir", action="store", type="string", dest="outdir",
                  help="final output directory")

(options, args) = parser.parse_args()

def LipoP(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	for i in range(len(data)):
		temp=data[i].split(" ")
		data[i]=[temp[1],"LipoP",";".join(temp[2:])+";"]

	return(data)

def deepArg(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	header=data[0].split("\t")
	header[0]=header[0][1:]
	data=data[1:]
	for i in range(len(data)):
		temp=data[i].split("\t")
		col3=""
		for j in range(len(header)):
			if(j!=3):
				col3+=header[j]+"="+temp[j]+";"
		data[i]=[temp[3],"deepArg",col3]
	
	return(data)

def eggDia(inFile):
	with open(inFile, "r") as INPUT:
		data=INPUT.read().strip().split("\n")

	header=data[3].split("\t")
	header[0]=header[0][1:]
	data=data[4:]
	data=data[:-3]
	for i in range(len(data)):
		temp=data[i].split("\t")
		col3=""
		for j in range(len(header)):
			if(j!=0):
				col3+=header[j]+"="+temp[j]+";"
		data[i]=[temp[0],"eggnogDiamond",col3]

	return(data)

def tmhmm(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	for i in range(len(data)):
		temp=data[i].split("\t")
		data[i]=[temp[0],"TMHMM",";".join(temp[1:])+";"]

	return(data)

def signalp(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	header=data[1].split("\t")
	data=data[2:]

	for i in range(len(data)):
		col3=""
		temp=data[i].split("\t")
		for j in range(len(header)):
			if(j!=0):
				col3+=header[j]+"="+temp[j]+";"
		data[i]=[temp[0],"signalp",col3]

	return(data)

def phobius(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	header=data[0].split("\t")
	data=data[1:]

	for i in range(len(data)):
		col3=""
		temp=data[i].split("\t")
		for j in range(len(header)):
			if(j!=0):
				col3+=header[j]+"="+temp[j]+";"
		data[i]=[temp[0],"phobius",col3]

	return(data)

def uclust(inFile):
	with open(inFile,"r") as INPUT:
		lines=INPUT.read().split("\n")
	
	lengths={}
	index={}

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

	return(index)

def door2(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	for i in range(len(data)):
		temp=data[i].split("\t")
		data[i]=[temp[0],"door2","target="+temp[1]+";start="+temp[2]+";stop="+temp[3]+";score="+temp[4]+";percentID="+temp[5]+";coverage="+temp[6]+";operonID="+temp[7]+";COG="+temp[8]+";"]

	return(data)

def card(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	for i in range(len(data)):
		temp=data[i].split("\t")
		data[i]=[temp[0],"card","start="+temp[1]+";stop="+temp[2]+";queryLength="+temp[3]+";alignLength="+temp[4]+";coverage="+temp[5]+";percentID="+temp[6]+";e-value="+temp[7]+";stitle="+temp[8]+";"]

	return data

def vfdb(inFile):
	with open(inFile,"r") as INPUT:
		data=INPUT.read().strip().split("\n")

	for i in range(len(data)):
		temp=data[i].split("\t")
		data[i]=[temp[0],"vfdb","start="+temp[1]+";stop="+temp[2]+";queryLength="+temp[3]+";alignLength="+temp[4]+";coverage="+temp[5]+";percentID="+temp[6]+";e-value="+temp[7]+";stitle="+temp[8]+";"]

	return data

lipoOutput=LipoP(options.LipoP_File)
deepArgOutput=deepArg(options.deepArg_File)
eggnogOutput=eggDia(options.eggnogDiamond_File)
tmhmmOutput=tmhmm(options.tmhmm_File)
signalpOutput=signalp(options.signalp_File)
phobiusOutput=phobius(options.phobius_File)
door2Output=door2(options.door2_File)
cardOutput=card(options.card_File)
vfdbOutput=vfdb(options.vfdb_File)

clusterIndex=uclust(options.uc_File)

### time to apply annotations to all members of a cluster now that we have an index

data={}

for i in lipoOutput:
	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del lipoOutput

for i in deepArgOutput:
	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del deepArgOutput

for i in cardOutput:
	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del cardOutput

for i in vfdbOutput:
	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del vfdbOutput

for i in eggnogOutput:
	for j in clusterIndex[i[0]]:

		m=re.search("(SRR\d+)_(.*)",j)

		if(m.group(1) in data):
			if(m.group(2) in data[m.group(1)]):
				data[m.group(1)][m.group(2)][i[1]]=i[2]
			else:
				data[m.group(1)][m.group(2)]={}
				data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)]={}
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]		

	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del eggnogOutput

for i in tmhmmOutput:
	for j in clusterIndex[i[0]]:
		m=re.search("(SRR\d+)_(.*)",j)

		if(m.group(1) in data):
			if(m.group(2) in data[m.group(1)]):
				data[m.group(1)][m.group(2)][i[1]]=i[2]
			else:
				data[m.group(1)][m.group(2)]={}
				data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)]={}
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]		

	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del tmhmmOutput

for i in signalpOutput:
	for j in clusterIndex[i[0]]:
		m=re.search("(SRR\d+)_(.*)",j)

		if(m.group(1) in data):
			if(m.group(2) in data[m.group(1)]):
				data[m.group(1)][m.group(2)][i[1]]=i[2]
			else:
				data[m.group(1)][m.group(2)]={}
				data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)]={}
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]		

	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del signalpOutput

for i in phobiusOutput:
	for j in clusterIndex[i[0]]:
		m=re.search("(SRR\d+)_(.*)",j)

		if(m.group(1) in data):
			if(m.group(2) in data[m.group(1)]):
				data[m.group(1)][m.group(2)][i[1]]=i[2]
			else:
				data[m.group(1)][m.group(2)]={}
				data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)]={}
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]		

	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del phobiusOutput

for i in door2Output:
	for j in clusterIndex[i[0]]:
		m=re.search("(SRR\d+)_(.*)",j)

		if(m.group(1) in data):
			if(m.group(2) in data[m.group(1)]):
				data[m.group(1)][m.group(2)][i[1]]=i[2]
			else:
				data[m.group(1)][m.group(2)]={}
				data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)]={}
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]		

	m=re.search("(SRR\d+)_(.*)",i[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][i[1]]=i[2]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][i[1]]=i[2]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][i[1]]=i[2]

del door2Output

#### opening the gff files and reading all useful info

with open(options.gff_File,"r") as INPUT:
	lines=INPUT.read().strip().split("\n")

info={}

for line in lines:
	temp=line.split("\t")

	m=re.search("(SRR\d+)_(.*)",temp[0])

	if(m.group(1) in data):
		if(m.group(2) in data[m.group(1)]):
			data[m.group(1)][m.group(2)][temp[1]]=temp[8]
		else:
			data[m.group(1)][m.group(2)]={}
			data[m.group(1)][m.group(2)][temp[1]]=temp[8]
	else:
		data[m.group(1)]={}
		data[m.group(1)][m.group(2)]={}
		data[m.group(1)][m.group(2)][temp[1]]=temp[8]

	if(m.group(1) in info):
		info[m.group(1)][m.group(2)]=temp[2:8]
	else:
		info[m.group(1)]={}
		info[m.group(1)][m.group(2)]=temp[2:8]

del lines

#### writing everything into 1 gff file per sample

for i in data:
	print(i)
	with open(options.outdir+"/"+i+".gff","w+") as OUTPUT:
		for j in data[i]:
			# print(j)
			for k in data[i][j]:
				# print(k)
				OUTPUT.write(j+"\t"+k+"\t"+"\t".join(info[i][j])+"\t"+data[i][j][k]+"\n")