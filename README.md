#"""author = Yeming May-06-2019"""

Structure of Single Sperm fastq reads:


Read 1: Sample reads.

@NB501319:122:HCMW7AFXY:1:11101:8697:1044 1:N:0:CCGTCC
AAACCACAGCCAAGGGAACGGGCTTGGCGGAATCAGCGGGGAAAGAAGACCCTGTAGAGCTTGACTCTAGTATGGC
+
AAA/AEEEEE/EE6/E6E//EA/EEA6/AEEEA/E/E///EEEAAEE66/E</A<//A/A/<EEEAE<EE/EEEEA


Read 2: Index reads. 

1st to 6th: barcode, 6nt, TAACCC 
8th to 15th: UMI, 8nt, TGTGGACT

@NB501319:122:HCMW7AFXY:1:11101:8697:1044 2:N:0:CCGTCC
TAACCCTGTGGACTTTTTTTTTTTTTTTTTTTTTAAAACAAAAAACAACAAACAAAAAAAAAAAAAGGAAAAAGG
+
AAAA<AE/A//AAEEEE<AEEEAEEEEEEEA/A////////////////<//////A//6/E//A//////////


Part or all of the 96 barcodes with known sequence are used in the library construction. (Sequence text file supplied by in the folder "barcode").




Steps from raw reads to data visualization:


Step 1. Combine lane reads

Combine NextSeq raw reads from 4 lane to generate Read 1 and Read 2 for each sample. This step is not demonstrated in the example.

In the "test_data" folder, the "test_R1.fq" and "test_R2.fq" are the first 25000 reads of combined Read 1 and Read 2 from one mouse sample.



Step 2. Merge Read1 and Read2

Merge Read 1 and Read 2. To combine the two reads file, the barcode and UMI sequence information will be preserved in the SeqID line of Read 1.


In the example, decompress "test_data.zip". Read 1 and Read 2 are provided in the "test_data" folder.

Run the "ReadMerge.py" with the following command:
python ReadMerge.py ./test_data/test_R1.fq ./test_data/test_R2.fq 6 8 ./merged_test_fq"

Input method: python ReadMerge.py [path/read1.fq] [path/read2.fq] [barcodeSize] [umiSize] [optional output directory]


Output:
Here the merged read file will be generated in the folder "merged_test_fq".



Step 3. Split barcode

Split individual sperm reads (split reads) out of the pool (merged reads) based on the given barcodes (96 barcodes).


In the example, Read 1 and Read 2 are provided in the "test_data" folder. Given barcode sequence is provided in the "barcode" folder.

Run the "BarcodeSplit.py" with the following command:
python BarcodeSplit.py ./merged_test_fq/Merged_test_R1.fq ./barcode/96_barcode split_test_fq stats

Input method: python BarcodeSplit.py [path/merged_sample_fastq] [path/barcode_file] [split sample output dir] [optional stats output dir]


Output:
In the terminal basic statistics of the known barcodes number of the barcode file, reads number of merged sample fastq, and known barcode reads number in the merged sample fastq  will be reported.

yemingxs-MacBook-Air:Single_Sperm_barcode_split yemingx$ ./example.sh 
Total known barcode: 96
Total reads: 25000
Total known barcode reads: 18861

The basic statistics of #read, #UMI and #barcode for each individual sample will be reported in the folder "stats"

The split reads fastq files will be generated in the folder "split_test_fq".


Notes:
Input and output directories and folder names in Step 2 and Step 3 are flexible based on the input options.

To test the python scripts in Step 2 and Step 3, make "example.sh" executable and run the script:
sudo chmod 755 example.sh
./example.sh

The output files should be the same as files in the folder "test_data_results".



Step 4. Alignment and count

Perform large RNA (fragmented library) or small RNA alignment (unfragmented library) for the split sample fastq files. In the example, the individual sperm fastq files are stored in the folder "split_test_fq". Each barcode represents one individual sperm.

For large RNA, I used Trimmomatic to trim reads, hisat2 for the alignment and featureCounts to generate count matrix.

Since the usable reads from the Single Sperm Sequencing are always, I recommend using the following parameters for high sensitivity hisat2 alignment:
hisat2 -N 1 -L 20 -i S,1,0.5 -D 25 -R 5 --pen-noncansplice 12 --mp 1,0 --sp 3,0

I used default parameters for Trimmomatic and featureCounts.


Note:
96 barcodes may not ALL used for one library. Need to ask the library construction personnel each time that how many barcodes used for each large RNA/small RNA library. 

If 48 random barcodes from the 96 given barcodes are used for one library, I will sort out the top 48 barcodes based on the reads number in the file "stats/Merged_test_R1.fq_countSum.txt". Then use these barcodes for the count analysis.


For small RNA, only keep the first 20 nt fastq sequence for the alignment. The small RNA library construction methodology is still under optimization.



Step 5. Visualization

The large RNA or small RNA count matrix will be processed by the single cell R workflow. Some data cleaning, quality control, and data visualization will be performed. One popular WorkFlow R workflow can be found in the following link. The workflow is well explained and updated frequently.

https://www.bioconductor.org/packages/release/workflows/html/simpleSingleCell.html


Other similar workflow can be used as well.

https://hemberg-lab.github.io/scRNA.seq.course/index.html