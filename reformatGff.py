#!/usr/bin/env python
import sys
from subprocess import check_call

with open(sys.argv[1], 'r') as fp1:
        data = fp1.read().strip().split('\n')

for i in range(len(data)):
        data[i] = data[i].split('\t')
        if data[i][1] == 'GeneMark.hmm':
                new_col1 = ''.join(data[i][8].split('id='))
                new_col9 = data[i][0]

                data[i][0] = sys.argv[1]+new_col1
                data[i][8] = new_col9
        else:
                temp=data[i][8].split(';')
                (data[i][0],temp[0])=(temp[0],data[i][0])
                data[i][0]=sys.argv[1]+'prodigal_'.join(data[i][0].split('ID='))
                data[i][8]=";".join(temp)

with open(sys.argv[1]+".reformatted", 'w') as fp2:
        fp2.write('\n'.join('\t'.join(x)for x in data))

check_call(["sed","-ri","s/\.gff/_/g",sys.argv[1]+".reformatted"])
