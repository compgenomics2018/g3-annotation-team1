#!/usr/bin/env python

# Comp Genomics 7210 
# Spring 2018
# Functional Annotation Team 1

import sys
import subprocess as sub

# Usage: ./gff2fasta.py <SRR#> <output filename>
# Notes: add getopts later (if needed)
#	produces .fna and .faa from Gene Prediction's GFF files

def reverse_complement(dna):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join([complement[base] for base in dna[::-1]])

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
outN = open("negative.fasta", "w")
outP = open("positive.fasta","w")
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
				outP.write("\n")			

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
				seq=reverse_complement(seq)
				outN.write(seq)
				outN.write("\n")

# Done writing to temp files
outN.close()
outP.close()

with open("positive.fasta","r") as p:
	fml=p.read()

with open("negative.fasta","r") as n:
	fml+=n.read()

with open(outFile+".fna","w") as o:
	o.write(fml)


# Convert nucleic acid sequence to amino acid sequence
print("Done parsing GFF\n\nTranslating "+outFile+" to protein sequence\n\n")
# Run EMBOSS transeq
sub.run(["transeq",outFile+".fna",outFile+".faa"])

sub.check_call(["rm","negative.fasta"])
sub.check_call(["rm","positive.fasta"])
sub.check_call(["rm","temp.fasta"])

print("DONE")
