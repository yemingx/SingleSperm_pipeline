##input: python BarcodeSplit.py [path/merged_sample_fastq] [path/barcode_file] [split sample output dir] [optional stats output dir]
##input example: python BarcodeSplit.py ./merged_test_fq/Merged_test_R1.fq ./barcode/96_barcode split_test_fq stats
#"""author = Yeming May-06-2019"""

import re
import sys
import os
import csv
import operator

#read merged sample file
with open(sys.argv[1],'r') as f1:
	Rmerge = f1.read().split('\n')
pathname = os.path.split(sys.argv[1])
#read barcode, store in barcode_set
with open(sys.argv[2],'r') as f2:
	barcodeListRaw = f2.read().split('\n')
barcodeList=barcodeListRaw[:-1]
#get sample directory
path = sys.argv[3]
#make output dir
if not os.path.exists(sys.argv[3]):
	os.makedirs(sys.argv[3])

#store barcode reads and barcode/UMI count in dictionary for each barcode read
dict_barcode={}
dict_count={}
dict_umi={}

for item in barcodeList:
	dict_barcode[item]=[]
	dict_count[item]=0
	dict_umi[item]=[]

TotalKnownBarcode=0
TotalRead=0
for i in range(0,len(Rmerge)):
	if Rmerge[i].startswith('@') and Rmerge[i+2].startswith('+'):
		item=Rmerge[i].split()
		seqid=item[0]
		barcode=item[1]
		UMI=item[2]
		if barcode in barcodeList:
			dict_barcode[barcode].append('\n'.join(Rmerge[i:i+4]))
			dict_count[barcode]+=1
			TotalKnownBarcode+=1
			if UMI not in dict_umi[barcode]:
				dict_umi[barcode].append(UMI)
		TotalRead+=1

print 'Total known barcode: ' + str(len(barcodeList))
print 'Total reads: ' + str(TotalRead)
print 'Total known barcode reads: ' + str(TotalKnownBarcode)

#output individual samples 
for key in dict_barcode:
	sample=open(os.path.join(path,key+'_'+pathname[-1]),'w')
	sample.write('\n'.join(dict_barcode[key]))
	sample.close

#output count summary
if len(sys.argv) == 5:
	if not os.path.exists(sys.argv[4]):
		os.system('mkdir {}'.format(sys.argv[4]))
	summary=open(os.path.join(sys.argv[4],pathname[-1]+'_countSum.txt'),'w')
else:
	summary=open(pathname[-1]+'_countSum.txt','w')


summary.write('barcode' + '\t' + '#read' + '\t' + '#read/TotalKnownBarcode' + 
	'\t' + '#read/TotalRead' + '\t' + '#UMI')
for key in sorted(dict_count, key=dict_count.get, reverse=True):
	summary.write('\n' + key + '\t' + str(dict_count[key]) + '\t' + 
		str(float(dict_count[key])/float(TotalKnownBarcode)) + '\t' +
		str(float(dict_count[key])/float(TotalRead)) + '\t' +
		str(len(dict_umi[key])))
