##input: python ReadMerge.py [path/read1.fq] [path/read2.fq] [barcodeSize] [umiSize] [optional output directory]
##input example: python ReadMerge.py ./test_data/test_R1.fq ./test_data/test_R2.fq 6 8 ./merged_test_fq
#"""author = Yeming May-06-2019"""

import re
import sys
import os


#read R1 sample file
with open(sys.argv[1],'r') as f1:
	R1 = f1.read().split('\n')

pathname = os.path.split(sys.argv[1])


#read R2 1-6 UMI 7-14
with open(sys.argv[2],'r') as f2:
	R2 = f2.read().split('\n')

barcodeSize=int(sys.argv[3])
umiSize=int(sys.argv[4])

#output merged Read
outputID = 'Merged_' + pathname[-1]
if len(sys.argv) == 6:
	if not os.path.exists(sys.argv[5]):
		os.system('mkdir {}'.format(sys.argv[5]))
	Rmerge = open(os.path.join(sys.argv[5],outputID),'w')
else:
	Rmerge = open(outputID,'w')

#merge R1 R2
if len(R1) != len(R2):
	print 'Error: Length of R1 does not match length of R2.'
else:
	for i in range(0,len(R1)):
		if R1[i].startswith('@') and R1[i+2].startswith('+'):
			seqID1=R1[i].split()[0]
			seqID2=R2[i].split()[0]
			if seqID1 == seqID2:
				Rmerge.write(R1[i].split()[0] + ' ' + R2[i+1][0:barcodeSize] 
					+ ' ' + R2[i+1][barcodeSize:barcodeSize+umiSize] + '\n')
				Rmerge.write(R1[i+1]+'\n'+R1[i+2]+'\n'+R1[i+3]+'\n')
Rmerge.close
