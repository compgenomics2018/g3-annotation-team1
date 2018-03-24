#!/usr/bin/bash

infile="/projects/home/sgulati36/skesaShit/$1"
outfile="/projects/home/sgulati36/pilerOutputs/$1"

pilercr -noinfo -in $infile -out $outfile
