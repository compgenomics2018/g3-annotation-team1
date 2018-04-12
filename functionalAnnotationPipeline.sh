#!/bin/bash

usage() { #change the options to correct options
        echo "Usage: ./functionalAnnotationPipeline.sh [OPTIONS] [ARGUEMENTS]

-f (Mandatory option) Absolute path to directory having the .fna and .faa files
-g (Mandatory option) Absolute path to directory having the .gff files
-o (Mandatory option) Absolute path to the output directory
-t door2 table file path
-i door2 gid file path
-d door2 database file path
-c card database file path
-v vfdb database file path
-h Help"
}

######################################################################################################################################################
# GetOpts part
######################################################################################################################################################
f=0;g=0;o=0;
table="kleb_all.opr";
gid="kleb_gid.txt";
database="kop_final.table";
card="protein_fasta_protein_homolog_model.fasta"
vfdb="VFDB_setB_nt.fas"

while getopts ":f:g:o:h" opt; do #change to actual options that are being used
  case ${opt} in
    f ) fastaPath=$OPTARG;f=1;
        if [ ! -d $fastaPath ] #checking if input file1 exists
        then
                echo "Directory \"$fastaPath\" does not exist";
                exit 1;
        fi
      ;;
    g ) gffPath=$OPTARG;g=1;
        if [ ! -d $gffPath ] #checking if input file2 exists
        then
                echo "Directory \"$gffPath\" does not exist";
                exit 1;
        fi
      ;;
    t ) table=$OPTARG;
      ;;
    i ) gid=$OPTARG;
      ;;
    d ) database=$OPTARG;
      ;;
    c ) card=$OPTARG;
      ;;
    v ) vfdb=$OPTARG;
      ;;
    o ) outDirectory=$OPTARG;o=1;
        if [ -d $outDirectory ] #checking if output file already exists
        then
                echo "Directory \"$outDirectory\" already exists, do you want to overwrite the existing directory? (y/n)";
                read reply #taking input from user
                if [ "$reply" == "n" ]
                  then
                    echo "Exiting"; #Exiting if user does not want to overwrite the existing file
                    exit 1
                  elif [ "$reply" != "y" ] #if user enters incorrect reply, the script will exit, if user enters "y" then the script will continue
                    then
                      echo "Invalid response ....... Exiting";
                      exit 1;
                  else
                    # echo "Okay";
                  	rm -rf $outDirectory;
                fi
        fi
      ;;
    h ) usage;exit
      ;;
    \? ) echo "Invalid option: $OPTARG" #checking for incorrect mills file name
         usage
         exit 1
      ;;
    : ) echo "Invalid usage: $OPTARG requires an argument"
        usage
        exit 1
      ;;
  esac
done

if [[ f -eq 0 ]] || [[ g -eq 0 ]] || [[ o -eq 0 ]]; then
	echo -e "Missing mandatory arguement, exiting.\n";usage;exit 1;
fi

######################################################################################################################################################
# Pre-processing of input files
######################################################################################################################################################

mkdir $outDirectory;
mkdir $outDirectory/temp;

cd $gffPath;

ls *.gff | xargs -n1 -P10 -t reformatGff.py

mv *.reformatted $outDirectory/temp/;
cd $outDirectory/temp;

ls *.reformatted | sed -e 'p;s/\.reformatted//g' | xargs -n2 mv;


cd $fastaPath;

ls *.faa | xargs -n1 -P10 -t reformatFasta.py; 
ls *.fna | xargs -n1 -P10 -t reformatFasta.py;

mv *_reformatted $outDirectory/temp/;
cd $outDirectory/temp;

ls *_reformatted | sed -e 'p;s/_reformatted//g' | xargs -n2 mv ;

######################################################################################################################################################
# Clustering of input files
######################################################################################################################################################

ls *.fna | xargs awk '{print $0;}' > mergedNucleotide.fasta
ls *.faa | xargs awk '{print $0;}' > mergedProtein.fasta
ls *.gff | xargs awk '{print $0;}' > mergedGff
mv mergedGff mergedGff.gff

usearch -cluster_fast mergedNucleotide.fasta -centroids mergedNucleotide.cent -uc mergedNucleotide.uc -id 0.99 -sort length;

getFastaHeaders.sh mergedNucleotide.fasta
extractSequences.py mergedProtein.fasta mergedNucleotide.fasta.headers
rm mergedNucleotide.fasta.headers
mv mergedNucleotide.fasta.headers.fasta centroidsProtein.fasta

######################################################################################################################################################
# Running tools
######################################################################################################################################################

source activate py27

emapper.py -i centroidsProtein.fasta --output finalRun -m diamond --usemem

deepARG.py --align --type nucl --input mergedNucleotide.fasta --out mergedNucleotide.out

source deactivate py27

phobius.pl -short centroidsProtein.fasta > phobius.out

LipoP -short -mergedProtein.fasta > lipo.out

tmhmm -short -centroidsProtein.fasta > tmhmm.out

signalp -t gram- -f short centroidsProtein.fasta > signalp.out

makeblastdb -in $vfdb -dbtype nucl -out vfdb
blastn -query mergedNucleotide.fasta -db vfdb -max_hsps 2 -max_target_seqs 2 -outfmt "6 qseqid qstart qend qlen length qcovs pident evalue stitle" -out vfdb.out
awk '{if($6>=90 && $7>=90) print $0}' vfdb.out >vfdb9090.out

makeblastdb -in $card -dbtype prot -out card
blastp -query mergedProtein.fasta -db card -max_hsps 2 -max_target_seqs 2 -outfmt "6 qseqid qstart qend qlen length qcovs pident evalue stitle" -out card.out
awk '{if($6>=90 && $7>=90) print $0}' card.out >card9090.out

door2.pl -i centroidsProtein.fasta -o door2.out -p 90 -i 90 -t $table -g $gid -d $database

######################################################################################################################################################
# Merging anntations from tools
######################################################################################################################################################

outputParser.py -l lipop.out -d larged_merged_nucl.out.mapping.ARG -e finalRunDiamond.emapper.annotations -t tmhmm.out -s signalp.out -p phobius.out -u mergedNucleotide.uc -g mergedGff.gff -r door2.out -c card9090.out -v vfdb9090.out -o ..

######################################################################################################################################################
# Deleting all temporary files
######################################################################################################################################################

cd $outDirectory

# rm -rf temp/ # This will delete all temp files created during the entire pipeline