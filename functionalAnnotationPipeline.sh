#!/bin/bash

usage() { #change the options to correct options
        echo "Usage: ./functionalAnnotationPipeline.sh [OPTIONS] [ARGUEMENTS] 
-f Absolute path to directory having the .fna and .faa files
-g Absolute path to directory having the .gff files
-h Help"
}

######################################################################################################################################################
# GetOpts part
######################################################################################################################################################

while getopts ":f:g:" opt; do #change to actual options that are being used
  case ${opt} in
    f ) fastaPath=$OPTARG;
        if ! [ -f $file1 ] #checking if input file1 exists
        then
                echo "Directory \"$file1\" does not exist"
                exit 1
        fi
      ;;
    g ) gffPath=$OPTARG;
        if ! [ -f $file2 ] #checking if input file2 exists
        then
                echo "Directory \"$file2\" does not exist"
                exit 1
        fi
      ;;
    # r ) ref_file=$OPTARG;r=1;
    #     if ! [ -f $ref_file ] #checking if reference genome file exists
    #     then
    #             echo "File \"$ref_file\" does not exist"
    #             exit 1
    #     fi
    #   ;;
    # o ) out_file=$OPTARG;o=1;
    #     if [ -f $out_file ] #checking if output file already exists
    #     then
    #             echo "File \"$out_file\" already exists, do you want to overwrite the existing file? (y/n)"
    #             read reply #taking input from user
    #             if [ "$reply" == "n" ]
    #               then
    #                 echo "Exiting" #Exiting if user does not want to overwrite the existing file
    #                 exit 1
    #               elif [ "$reply" != "y" ] #if user enters incorrect reply, the script will exit, if user enters "y" then the script will continue
    #                 then
    #                   echo "Invalid response ....... Exiting"
    #                   exit 1
    #             fi
    #     fi
    #   ;;
    # e ) realign_flag=1;
    #   ;;
    # f ) mills_file=$OPTARG;f=1;
    #   ;;
    # z ) gz_flag=1;
    #   ;;
    # v ) v_flag=1;
    #   ;;
    # i ) index_flag=1;
    #   ;;
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


######################################################################################################################################################
# Pre-processing of input files
######################################################################################################################################################

cd $gffPath;
currentDir="$(pwd)";
echo "In "$currentDir;
ls *.gff | xargs -n1 -P10 -t reformatGff.py
mkdir temp;
mv *.reformatted temp/;
cd temp;
currentDir="$(pwd)";
echo "In "$currentDir;
ls *.reformatted | sed -e 'p;s/\.reformatted//g' | xargs -n2 mv;


cd $fastaPath;
currentDir="$(pwd)";
echo "In "$currentDir;
ls *.faa | xargs -n1 -P10 -t reformatFasta.py; 
ls *.fna | xargs -n1 -P10 -t reformatFasta.py;
mkdir temp;
mv *_reformatted temp/;
cd temp;
currentDir="$(pwd)";
echo "In "$currentDir;
ls *_reformatted | sed -e 'p;s/_reformatted//g' | xargs -n2 mv ;
ls *.fna | xargs cat > mergedNucleotide.fasta
ls *.faa | xargs cat > mergedProtein.fasta
# usearch -cluster_fast mergedNucleotide.fasta -centroids mergedNucleotide.cent -uc mergedNucleotide.uc -id 0.99;




######################################################################################################################################################
# Clustering of input files
######################################################################################################################################################


######################################################################################################################################################
# Running tools
######################################################################################################################################################


######################################################################################################################################################
# Merging anntations from tools
######################################################################################################################################################


######################################################################################################################################################
# Mapping cluster annotations to individual GFFs
######################################################################################################################################################


######################################################################################################################################################
# Deleting all temporary files
######################################################################################################################################################
