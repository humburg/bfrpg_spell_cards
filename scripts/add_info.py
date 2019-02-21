"""
Add additional information to spells. The output file consists of spell records that have
been augment with spell specific entries from a second file. Spells are identified by name.

Both input files are assumed to be in json format.

Usage: add_info.py [options] <spells> <info> <output>

Options:
  --warn-missing  Generate a warning for each spell in <spells> that doesn't have a corresponding entry in <info>.
"""

import json
import os
from docopt import docopt

opts = docopt(__doc__)

spells = json.load(open(opts["<spells>"]))
info = json.load(open(opts["<info>"]))

for i in range(len(spells)):
    if spells[i]["name"] in info:
        spell_info = info[spells[i]["name"]]
        spells[i] = {**spells[i], **spell_info}
    elif opts["--warn-missing"]:
        print("Missing spell info for " + spells[i]["name"])

os.makedirs(os.path.dirname(opts["<output>"]), exist_ok=True)
out_file = open(opts["<output>"], "w")
json.dump(spells, out_file, indent=2)
