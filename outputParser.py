#!/usr/bin/env python

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
				print(temp)
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
	print(len(header))
	print(len(data[0].split("\t")))

	for i in range(len(data)):
		col3=""
		temp=data[i].split("\t")
		for j in range(len(header)):
			if(j!=0):
				col3+=header[j]+"="+temp[j]+";"
		data[i]=[temp[0],"phobius",col3]

	return(data)

# lipoOutput=LipoP(options.LipoP_File)
# deepArgOutput=deepArg(options.deepArg_File)
# eggnogOutput=eggDia(options.eggnogDiamond_File)
# tmhmmOutput=tmhmm(options.tmhmm_File)
# signalpOutput=signalp(options.signalp_File)
# phobiusOutput=phobius(options.phobius_File)
