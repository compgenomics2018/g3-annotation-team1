#!/usr/bin/env python

# Comp Genomics 7210 
# Spring 2018
# Functional Annotation Team 1

import sys
import subprocess as sub

# Usage: ./gff2fasta.py <SRR#> <output filename>
# Notes: add getopts later (if needed)
#	produces .fna and .faa from Gene Prediction's GFF files

if len(sys.argv) < 3:
	print("Incorrect number of arguments")
	exit(0)

# Files required to extract sequence from FASTA for genes annotated in GFF
fastaFile = "/projects/data/team1_GenePrediction/assemblies_all/skesaoutput/"+sys.argv[1]+".skesa.fa"
gffFile = "/projects/data/team1_GenePrediction/Prodigal_output_all/output/"+sys.argv[1]+".output.gff"
# Output file
outFile = sys.argv[2]

# Read in FASTA and GFF file from Gene Prediction directories
# with open(fastaFile, "r") as f:
#  fasta = f.read()
with open(gffFile, "r") as g:
	gff = g.read()

# Start writing to output file
outN = open("negative.fasta", "a")
outP = open("positive.fasta","a")
print("Parsing GFF file "+gffFile)

for i in gff.split("\n"):
 # Skip header information
	if i.find("#") != 0:
 # array positions 3 & 4 contains start & end positions, respectively
		parse = i.split("\t")
		if len(parse) == 1:
			break
  # Define parameters required to run samtools faidx
		seqname = parse[0]
		start = parse[3]
		end = parse[4]
		if(parse[6]=="+"):
			# Run samtools with parsed parameters to store the positive strand sequences in a file
			temp = open("temp.fasta","w")
			sub.Popen(["samtools","faidx",fastaFile, seqname+":"+start+"-"+end], stdout=temp)
			temp.close()
			seq=""
			with open("temp.fasta","r") as INPUT:
				for line in INPUT:
					if(">" in line):
						outP.write(line)
					else:
						seq+=line.strip()
				outP.write(seq)			

		elif(parse[6]=="-"):
			# Run samtools with parsed parameters to store the negative strand sequences in a different file
			temp = open("temp.fasta","w")
			sub.Popen(["samtools","faidx",fastaFile, seqname+":"+start+"-"+end], stdout=temp)
			temp.close()
			seq=""
			with open("temp.fasta","r") as INPUT:
				for line in INPUT:
					if(">" in line):
						outN.write(line)
					else:
						seq+=line.strip()
				seq=seq[::-1] # reversing the string
				seq=seq.replace("A","Z")
				seq=seq.replace("T","A")
				seq=seq.replace("Z","T")
				seq=seq.replace("G","Z")
				seq=seq.replace("C","G")
				seq=seq.replace("Z","C")
				outN.write(seq)

# Done writing to temp files
outN.close()
outP.close()

# Convert nucleic acid sequence to amino acid sequence
# print("Done parsing GFF\n\nTranslating "+outFile+" to protein sequence\n\n")
# Run EMBOSS transeq
# sub.run(["transeq",outFile+".fna",outFile+".faa"])
