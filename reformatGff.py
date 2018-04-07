#!/usr/bin/env python
import sys

with open(sys.argv[1], 'r') as fp1:
        data = fp1.read().strip().split('\n')

for i in range(len(data)):
        data[i] = data[i].split('\t')
        if data[i][1] == 'GeneMark.hmmd':
                new_col1 = ''.join(data[i][8].split('id='))
                new_col9 = data[i][0]

                data[i][1] = new_col1
                data[i][9] = new_col9
        else:
                temp=data[i][8].split(';')
                (data[i][0],temp[0])=(temp[0],data[i][0])
                data[i][0]='prodigal_'.join(data[i][0].split('ID='))
                data[i][8]=";".join(temp)

with open(sys.argv[1]+".reformatted", 'w') as fp2:
        fp2.write('\n'.join('\t'.join(x)for x in data))
