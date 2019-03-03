TEMPLATE=templates
DATA=core/edited
SCRIPT=python /usr/src/app/scripts/

.PHONY: all clean clean_all pdf png

all: pdf png
pdf: Cleric-spell-cards.pdf MU-spell-cards.pdf
png: cleric_png mu_png
clean_all: clean
	rm -f MU-spell-cards.pdf Cleric-spell-cards.pdf Cleric-cards/*.png MU-cards/*.png
	rm -rf Cleric-cards MU-cards
clean:
	rm -f MU-cards/*.pdf MU-cards/*.svg Cleric-cards/*.pdf Cleric-cards/*.svg 

ifeq ($(FIRST_PASS_DONE),)
Cleric-spell-cards.pdf: .cleric_dummy
	$(MAKE) FIRST_PASS_DONE=y Cleric-spell-cards.pdf
MU-spell-cards.pdf: .mu_dummy
	$(MAKE) FIRST_PASS_DONE=y MU-spell-cards.pdf

cleric_png: .cleric_dummy
	$(MAKE) FIRST_PASS_DONE=y $(patsubst %.svg,%.png,$(wildcard Cleric-cards/*.svg))
mu_png: .mu_dummy
	$(MAKE) FIRST_PASS_DONE=y $(patsubst %.svg,%.png,$(wildcard MU-cards/*.svg))

.cleric_dummy: $(DATA)/Cleric_short.json $(wildcard $(TEMPLATE)/Cleric_template*.svg)
	$(SCRIPT)create_cards.py -o Cleric-cards $(DATA)/Cleric_short.json $(TEMPLATE)/Cleric_template*.svg
.mu_dummy: $(DATA)/Magic-User_short.json $(wildcard $(TEMPLATE)/MU_template*.svg)
	$(SCRIPT)create_cards.py -o MU-cards $(DATA)/Magic-User_short.json $(TEMPLATE)/MU_template*.svg

else
CLERIC_SVG := $(wildcard Cleric-cards/*.svg)
CLERIC_PDF := $(patsubst %.svg,%.pdf,$(CLERIC_SVG))
MU_SVG := $(wildcard MU-cards/*.svg)
MU_PDF := $(patsubst %.svg,%.pdf,$(MU_SVG))

Cleric-spell-cards.pdf: $(CLERIC_PDF)
	$(SCRIPT)merge_pdf.py Cleric-spell-cards.pdf $(sort $^)

MU-spell-cards.pdf: $(MU_PDF)
	$(SCRIPT)merge_pdf.py MU-spell-cards.pdf $(sort $^)

%.pdf: %.svg
	$(SCRIPT)svg2pdf.py -o $(@D) --dpi=300 $?
%.png: %.svg
	$(SCRIPT)svg2png.py -o $(@D) --dpi=300 $?
endif
