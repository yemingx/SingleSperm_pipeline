#"""author = Yeming May-06-2019"""

#!/bin/bash
python ReadMerge.py ./test_data/test_R1.fq ./test_data/test_R2.fq 6 8 ./merged_test_fq
python BarcodeSplit.py ./merged_test_fq/Merged_test_R1.fq ./barcode/96_barcode split_test_fq stats
