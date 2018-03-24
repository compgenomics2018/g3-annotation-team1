#!/bin/bash

#Usage : ls * | xargs -n1 -P1 -I% -t getFastaHeaders.sh %
#Run the above command when in the folder containing the fasta files, this will extract all headers for a file called <filename> and store it in <filename>.headers 

awk '{if($1~/^>/){print $0}}' $1 > $1".headers"
