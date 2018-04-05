#! /bin/bash
 
# Usage : ls * | xargs -n1 -P1 -I% -t getFastaHeaders.sh %
# Run the above command when in the folder containing the gff files from gene predition team.
# The GFF files do not match the start position of fasta files and have an offset of 1 for start positions.
# This will reduce the start positions in the GFF file <filename> by 1 and store the updated file as adjusted_<filename>
# 1 line bash script is needed to run such commands using xargs, to redirect the output of every single awk call using xargs to a different file.
# If you just use ls | xargs awk and pipe this to a file, only the output of the last awk call will be saved.

awk 'BEGIN{OFS="\t"}{$4--;print$0}' $1 > "adjusted_"$1
