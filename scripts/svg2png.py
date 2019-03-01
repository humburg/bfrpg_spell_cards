#!/usr/local/bin/python

"""
Convert svg files to png. Requires inkscape to be installed and in the path.

Usage: svg2pdf.py [options] <svg>...

Options:
  --outdir <dir>, -o <dir>  Output directory for pdf files (will be created if it doesn't exist). [default: .]
  --strict  Stop if conversion errors are encountered. The default is to convert as many input files as possible.
  --dpi <dpi>  Resolution to use when rasterising filter effects. [default: 96]
"""

import os
import re
import subprocess
import sys
from docopt import docopt

opts = docopt(__doc__)

## Convert svg files to png with inkscape
os.makedirs(opts["--outdir"], exist_ok=True)
for filename in opts["<svg>"]:
    out_name = os.path.basename(filename)
    out_name = opts["--outdir"] + '/' + re.sub("\\.svg$", ".png", out_name)
    command = "inkscape --without-gui --export-png=" + out_name + " --file=" + filename + " --export-dpi=" + opts["--dpi"]
    try:
        completed = subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("stdout:", str(e.stdout))
        print("stderr:", str(e.stderr))
        if opts["--strict"]: raise

    