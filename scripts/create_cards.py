"""
Combine spell descriptions with card template(s) to create spell cards.

Usage: create_cards.py [options] <spells> <template>...
       create_cards.py --doc

Options:
  --doc  Show full documentation.
  --strict  Stop on warnings.
  --outdir <dir>, -o <dir>  Output directory [default: .].
"""

import copy
import json
import os
import sys
import re
import xml.etree.ElementTree as ET

from docopt import docopt

opts = docopt(__doc__)

full_doc = """
            Combine spell descriptions with card template(s) to create spell cards.

            The <spells> file should be in json format. Each spell record should have
            (at least) the fields 'name', 'range', 'duration', 'class', 'level', 'description',
            'book' and 'page'. All json fields will be matched to corresponding elements in
            the template, if present. The elements to be populated are expected to have an
            attribute 'template_label' matching the name of the json field. The only exception
            to this rule is a possible template_label 'reference', which will be replaced with
            the combined values of 'book' and 'page'.

            Template files are assumed to have names of the form <class>_template[_suffix].svg,
            where <class> is the name of the spellcaster class and [_suffix] is an optional
            suffix identifying the type of template. For example, 'MU_template.svg' might
            be the name of the Magic-User card template and 'MU_template_back.svg' could
            be the name for the corresponding card back template.

            The names of output files will replace 'template' with spell level and name.
            For example, with the above templates the light spell will create the files
            'MU_L1_light.svg' and 'MU_L1_light_back.svg'.
            """

if opts["--doc"]: 
    print(full_doc)
    exit()

ns = {'svg':'http://www.w3.org/2000/svg'}

def format_text(text, span, ns):
    """
    Convert HTML text formatting into suitable svg elements.
    """
    tokens = re.split("</?strong>", text)
    elem = [ET.Element("{" + ns + "}"  + span) for t in tokens]
    for i in range(len(tokens)):
        elem[i].text = tokens[i]
        if i % 2:
            elem[i].set('style', 'font-weight:bold')
    return elem

def parse_text(text, paragraph="flowPara", span="flowSpan", ns="http://www.w3.org/2000/svg"):
    """
    Parses a text containing a subset of HTML and returns a list of xml Elements,
    suitable for inclusion in an SVG.

    Currently only the <p> and <strong> HTML tags are supported.
    """
    
    ## Split text into paragraphs
    text = re.split("</?p>", text)
    text = [t for t in text if len(t)]
    para = [ET.Element("{" + ns + "}"  + paragraph) for t in text]
    for i in range(len(text)):
        para[i].extend(format_text(text[i], span, ns))
    return para

## load the spells
spells = json.load(open(opts["<spells>"]))

## load templates
name_template = [re.split('template', os.path.basename(s)) for s in opts["<template>"]]
template = [ET.parse(f) for f in opts["<template>"]]

## create spell cards from templates
os.makedirs(opts["--outdir"], exist_ok=True)
for spell in spells:
    if 'reference' not in spell:
        spell["reference"] = spell["book"] + ' ' + spell["page"]
    for i in range(len(template)):
        card = copy.deepcopy(template[i])
        card_root = card.getroot()
        for field in spell:
            for elem in card_root.findall(".//*[@template_label='" + field + "']"):
                if elem.tag == '{' + ns['svg'] + '}flowRoot':
                    card_text = parse_text(spell[field])
                    elem.remove(elem.find('svg:flowPara', ns))
                    elem.extend(card_text)
                elif elem.tag == '{' + ns['svg'] + '}tspan':
                    elem.text = spell[field]
                else:
                    print("Template " + opts["<template>"][i] + " contains unexpected element with template label '" + \
                        field +"'. Expected 'flowRoot' or 'tspan', found '" + elem.tag + "'.", file=sys.stderr)
                    if opts["--strict"]: exit()
        simple_name = re.sub("\\*$", '', spell["name"].lower())
        simple_name = re.sub(" ", "_", simple_name)
        card_name = name_template[i][0] + 'L' + spell["level"] + '_' + \
                    simple_name + name_template[i][1]
        card.write(opts["--outdir"] + '/' + card_name)


