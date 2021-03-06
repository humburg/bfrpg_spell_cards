# Spell cards for the Basic Fantasy Role-playing Game

This repository contains resources and scripts to create spell cards for the [Basic Fantasy Role-playing game](https://www.basicfantasy.org/index.html).

## Available resources

Files are organised in directories according to the source they refer to. Currently, only spells from
the core rule book are available (in *core/*).

### Spells descriptions in JSON format

JSON formatted files with different versions of spell descriptions are available.

* **long**: These are the original spell descriptions that were extracted from the XML file (available in *downloads*).
* **referenced**: These files also contain the full length spell descriptions but references to page numbers in the source book have been added.
* **edited**: Files in this directory are derived from the referenced JSON files. Spell descriptions have been edited for length to ensure they
  are short enough to fit on cards.

### Templates

Card templates are designed for use with the *create_cards.py* script. A template contains all the art that is shared between the cards. In addition, it has text areas that are placeholders for card specific text.

## Creating your own cards

### Creating custom templates

A card template needs to adhere to a number of conventions. The name of the file should be of the form *`<type>`_template*, where *`<type>`* is indicating the type of card the template is for. If you are using separate templates for the face and back of the cards it is recommended to follow the name with *_[face]* and *_[back]* respectively.

A template may contain any number of template fields. For an element to be recognised as a template field it needs to have a *template_label* attribute. The value of this attribute is then matched to a field of the same name in the data file to provide card specific content. Template fields can be either `text` elements or `flowRoot` elements.

#### Using `<text>` elements

In the case of a text element the text contained within it will be replaced with text from the data file. All styling of the element will be retained but no additional formatting is supported.

#### Using `<flowRoot>` elements

Longer pieces of text are more conveniently stored in a `flowRoot` element that allows for automatic text wrapping. The first `flowPara` element of a `flowRoot` template field will be replaced with one or more paragraphs of text. Note that the existing element will be *replaced* and all element specific styling will be lost. To avoid this, apply styles to the `flowRoot` container.

Limited text formatting of card specific text is supported in `flowRoot` elements. Use `<p></p>` tags to create paragraphs and `<strong></strong>` for bold text.

### Creating custom data files

To create cards with your own content, prepare a JSON file with one object for each card you wish to create. Member names of these objects will be matched to the names of template fields. Entries that don't match a template field will be ignored when cards are created.

### Using Docker

The easiest way to set up the software environment required to create custom cards is to use the provided Dockerfile. If you have [Docker](https://www.docker.com/) installed on your machine you can build a Docker image with all the required software from this directory py typing `docker build -t spell_cards .` at the command-line. Once the image as been built, run

```docker run -ti --rm -v "/path/to/resources":/data spell_cards sh```

to launch the application. This will provide you with a Linux command-line interface to run python scripts in the `scripts/` directory. To create variants of the cards in this repository after modifying either the SVG templates or data files, simply change to the `/data` directory and run `make pdf` or `make png` to create new versions of the cards in PDF or PNG format as desired. Alternatively, run `make all` to create both. To create a different set of cards you can either modify the Makefile or use the python scripts directly.