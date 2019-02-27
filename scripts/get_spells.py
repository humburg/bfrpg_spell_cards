#!/usr/local/bin/python

"""
Download official spell descriptions and save them as yaml files.
Spells are split into one file per class.

Usage: get_spells.py [options]

Options:
  -s <file>, --source <file>  XML file with spell descriptions [default: https://www.dustinian.com/_prototypes/bfrpg_spell_cards.xml]
  -o <directory>, --output <directory>  Base directory for output [default: ./]
"""

import json
import os
import os.path
import re
import urllib.request
import xml.etree.ElementTree as ET

from docopt import docopt

opts = docopt(__doc__)

## Get input file
download_dir = opts["--output"] + 'download/'
download_target = download_dir + 'spells.xml'
os.makedirs(download_dir, exist_ok=True)

if os.path.isfile(download_target):
  print("File " + download_target + " already exists.")
else:
  print("Downloading spell descriptions from", opts["--source"], "to", download_target)
  urllib.request.urlretrieve(opts["--source"], download_target)

## parse spell descriptions and split them by class
print("Parsing spell descriptions...")
caster_spells = {}
root = ET.parse(download_target).getroot()
for spell in root.find('spells').findall('spell'):
    spell_class = spell.find("class").text.split(', ')
    for caster in spell_class:
        caster = caster.replace("Magic User", "Magic-User")
        [caster_class, caster_level] = caster.split()
        spell_descr = ""
        for para in spell.find('description'):
            spell_descr += ET.tostring(para, method="xml").decode()
        spell_descr = re.sub(r"\s+", " ", spell_descr)
        if caster_class not in caster_spells:
            caster_spells[caster_class] = []
        caster_spells[caster_class].append({'name':spell.find('name').text,
                                            'range':spell.find('range').text,
                                            'duration':spell.find('duration').text,
                                            'class':caster_class,
                                            'level':caster_level,
                                            'description':spell_descr,
                                            'source':opts["--source"]})

## create output files
out_dir = opts["--output"] + '/long/'
print("Writing output files to", out_dir)
os.makedirs(out_dir, exist_ok=True)
for caster_class in caster_spells.keys():
    print("  " + caster_class + ": " + caster_class + '_raw.json')
    caster_file = open(out_dir + caster_class + '_raw.json', mode="w")
    json.dump(caster_spells[caster_class], caster_file, indent=2)
    caster_file.close()
