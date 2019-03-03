TEMPLATE=templates
DATA=core/edited
SCRIPT=python /usr/src/app/scripts/

.PHONY: all clean clean_all pdf png cleric_png mu_png

all: pdf png
pdf: Cleric-spell-cards.pdf MU-spell-cards.pdf
png: cleric_png mu_png
clean_all: clean
	rm -f MU-spell-cards.pdf Cleric-spell-cards.pdf
clean:
	rm -rf MU-cards/pdf/* MU-cards/png/* MU-cards/* MU-cards Cleric-cards/pdf/* Cleric-cards/png/* Cleric-cards/* Cleric-cards

ifeq ($(FIRST_PASS_DONE),)
Cleric-spell-cards.pdf: .cleric_dummy
	$(MAKE) FIRST_PASS_DONE=y Cleric-spell-cards.pdf
MU-spell-cards.pdf: .mu_dummy
	$(MAKE) FIRST_PASS_DONE=y MU-spell-cards.pdf

cleric_png: .cleric_png_dummy
	$(MAKE) FIRST_PASS_DONE=y Cleric-cards/png/*.png

.cleric_dummy: $(DATA)/Cleric_short.json $(wildcard $(TEMPLATE)/Cleric_template*.svg)
	$(SCRIPT)create_cards.py -o Cleric-cards $(DATA)/Cleric_short.json $(TEMPLATE)/Cleric_template*.svg
.mu_dummy: $(DATA)/Magic-User_short.json $(wildcard $(TEMPLATE)/MU_template*.svg)
	$(SCRIPT)create_cards.py -o MU-cards $(DATA)/Magic-User_short.json $(TEMPLATE)/MU_template*.svg

.cleric_png_dummy: $(DATA)/Cleric_short.json $(wildcard $(TEMPLATE)/Cleric_template*.svg)
	$(SCRIPT)create_cards.py -o Cleric-cards $(DATA)/Cleric_short.json $(TEMPLATE)/Cleric_template*.svg
else
Cleric-spell-cards.pdf: Cleric-cards/pdf/*.pdf
	$(SCRIPT)merge_pdf.py Cleric-spell-cards.pdf $(sort $^)
Cleric-cards/%.svg: $(DATA)/Cleric_short.json $(TEMPLATE)/Cleric_template*.svg
	$(SCRIPT)create_cards.py -o Cleric-cards $(DATA)/Cleric_short.json $(TEMPLATE)/Cleric_template*.svg

MU-spell-cards.pdf: MU-cards/pdf/*.pdf
	$(SCRIPT)merge_pdf.py MU-spell-cards.pdf $(sort $^)
MU-cards/%.svg: $(DATA)/Magic-User_short.json $(TEMPLATE)/MU_template*.svg
	$(SCRIPT)create_cards.py -o MU-cards $(DATA)/Magic-User_short.json $(TEMPLATE)/MU_template*.svg

%.pdf: %.svg
	$(SCRIPT)svg2pdf.py -o $(@D) --dpi=300 $(subst pdf/,,$?)
%.png: %.svg
	$(SCRIPT)svg2png.py -o $(@D) --dpi=300 $(subst png/,,$?)
endif
