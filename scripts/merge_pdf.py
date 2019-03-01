#!/usr/local/bin/python

"""
Merge multiple PDF files into a single output file.

Usage: merge_pdf.py <merged_file> <pdf>...

Arguments:
  pdf  PDF files to merge.
  merged_file  Name of output file.
"""

import os
import PyPDF2
from docopt import docopt

opts = docopt(__doc__)

## merge all pdfs
os.makedirs(os.path.dirname(opts["<merged_file>"]), exist_ok=True)
merger = PyPDF2.PdfFileMerger()
for filename in opts["<pdf>"]:
    merger.append(filename)
merger.write(opts["<merged_file>"])
