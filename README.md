# Team 1 - Functional Annotation 

List of scripts in our GitHub repo.

 1. door2.pl -- script used to run door2
 2. extractSequences.py -- a script which extracts sequences from a fasta file based on a headers given in second file
 3. functionalAnnotationPipeline.sh -- the final pipeline
 4. getFastaHeaders.sh -- script which extracts all headers from a fasta file and stores in a new file
 5. outputParser.py -- script which parses the output of all tools, uClust and the original GFFs to create new GFFs with annotations
 6. parseUclustOutput.py -- script which reads in the .uc file generated from uClust and creates an index file and a sizes file
 7. pilerCr.sh -- script used to run pilerCR (not included in final pipeline)
 8. reformatFasta.py -- script which changes the gene names in the fasta file, reformats the file so that all sequences are in 1 line and also appends the SRR ID in front of the gene name.
 9. reformatGff.py -- script which changes column 1 of the GFF to the gene name and also appends the SRR ID in front of the gene name.

Other files in our GitHub repo are

 1. kleb_all.opr
 2. kleb_gid.txt
 3. kop_final.table
 4. protein_fasta_protein_homolog_model.fasta
 5. VFDB_setB_nt.fas

These are the default databases used for door2, CARD and VFDB.
