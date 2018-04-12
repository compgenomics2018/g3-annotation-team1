#!/usr/bin/env perl
use strict;
use warnings;
use Getopt::Long qw(GetOptions);
#the getopts with default values for the variables
my $input_file= "";
my $output_file="";
my $pidentity= 90;
my $coverage= 90;
my $table= "kleb_all.opr";
my $gid= "kleb_gid.txt";
my $database = "kop_final.table";
my $help = 0;
GetOptions(
	'i=s' => \$input_file,
	'o=s' => \$output_file,
	'p=i' => \$pidentity,
	'c=i' => \$coverage,
	't=s' => \$table,
	'g=s' => \$gid,
	'd=s' => \$database,
    'h!' => \$help,
) or die "Usage: $0 -i <input protein fasta> -o <output file> -d <blast database> -p <percent identity integer> -c <query coverage integer> 
-t <operon table file> -g <file containing gid and ncbi id data>\n";

if($help){
    print "Usage: $0 -i <input protein fasta> -o <output file> -d <blast database> -p <percent identity integer> -c <query coverage integer> 
-t <operon table file> -g <file containing gid and ncbi id data>\n";
    exit;
}



#create the operon hash
my %operon;
#open the file containing the combined operon tables
#grab the GID, OperonID, COG, and Product from the table
#concatenate them together with tab spaces and make the GID the key
#and the concatanated part the value
open(file_1 , '<', $table);
my @table = <file_1>;
foreach my $line (@table) {
	my @split = split(/\t/, $line);
	my $GID = $split[1];
	my $OID = $split[0];
	my $COG = $split[7];
	my $Prf = $split[8];
	my $concat = $OID."\t".$COG."\t".$Prf;
	$operon{$GID} = $concat;

}

close file_1;

#create the GID/NCBI ID hass
my %g_o;
#open the file containing each GID and its 
#respective NCBI ID and have the NCBI ID be the key
#and the GID be the value
open(file_2, '<', $gid);
# chomp $_;
my @table_2 = <file_2>;
foreach my $line (@table_2){
	my @splits = split(/\s+/, $line);
	my $GID_2 = $splits[0];
	my $Seq = $splits[1];
	$g_o{$Seq} = $GID_2;
}

close file_2;
#run blast on the database that was created by 
#the GIDs gathered from the operon table and wget was used to 
#populate the table from NCBI. And intermediate file is created to house the output of the
#blast search
my $out = "operon_intermediate.txt";
system("blastp -db $database -query '$input_file' -out $out -max_target_seqs 1 -max_hsps 1 -num_threads 6 -outfmt '6 qseqid sseqid qstart qend evalue pident qcovs'"
);

#this code opens the file containing the blast hits and
#filters them down based on the parameters of having a percent
#identity and query coverage at 80% or greater.
open(input_1, '<', "operon_intermediate.txt");
open(output_2, '>', "operon_output.txt");
my @file = <input_1>;
foreach my $line (@file){
	my @split = split(/\t/, $line);
	my $pident =$split[5];
	my $qcovs = $split[6];
	if($pident >= $pidentity && $qcovs >= $coverage){
		print output_2 $line;
	}
}
close input_1;
close output_2;

#open a temp file and also the final file that will be written to
open(input_2, '<', "operon_output.txt");
open(output_3, '>', $output_file);
# chomp $_;
#go through each line from the blast output
#grab the sseqid and look through the first %g_o hash table for 
#GID associated so then you can look up the concatenated value from the 
#%operon hash table to add it to the end of the blast output
#and write the combined output to the output file.
print output_3 "qseqid\tsseqid\tqstart\tqend\tevalue\tpident\tqcovs\tOperonID\tCOG\tProduct\n";
my @file_2 = <input_2>;
foreach my $line (@file_2){
	chomp $line;
	my @sp = split(/\t/, $line);
	my $Seq_2 = $sp[1];
	foreach my $h (keys %g_o){
		if($h =~ m/\Q$Seq_2/){
			foreach my $k (keys %operon){
				if($k =~ m/\Q$g_o{$h}/){
				print output_3 $line."\t".$operon{$k}."\n";	
				}

			}
		}
	} 
}
	close input_2;
	close output_3;


# #remove the temp file
system("rm operon_intermediate.txt");
system("rm operon_output.txt")
