SRC=p.tex

all: figures p.pdf
p.pdf: $(SRC)

p.odt: p.pdf
	/usr/share/tex4ht/oolatex p.tex '' '' '' '-interaction=nonstopmode'

figures:
	$(MAKE) -C figures

clean::
	rm -f revision.log *-stamp
	$(MAKE) -C figures clean
	-rm -f *.4ct *.4tc *.idv *.lg *.tmp p.odt *.xref


#
# Private parts: do not touch!
#
pdf: $(SRC:.tex=.pdf) $(SRC:.rst=.pdf)
bib: $(SRC:.tex=.bbl)

TEXFLAGS += -interaction=nonstopmode
PDFLATEX=TEXINPUTS=.:sty:$(TETEXSRC): pdflatex $(TEXFLAGS) -shell-escape
BSTDIR = sty
%.pdf %.aux: %.tex $(MSRC)
	rm -f $*.log
	@run=0; while ( [ ! -e "$*.log" ] || grep -q "Rerun to get" "$*.log" ) && [ $$run -lt 5 ]; do \
	     echo "** Re-running pdftex. Run $$run **";    \
		 $(PDFLATEX) $< >/dev/null 2>&1 || cat $*.log; \
		 run=$$(($$run+1)); \
    done

BIBTEX = bibtex
%.bbl: %.aux
	env BIBINPUTS=$(BIBDIR): BSTINPUTS=$(BSTDIR): $(BIBTEX) $(BIBFLAGS) $*

## Helper if interested in providing proper version tag within the manuscript
ASRC=$(SRC) $(MSRC) $(SSRC)
cleanexts=dvi aux bbl blg end ps pdf djvu log idx toc lot lof ttt tpt fff out nav snm vrb cb cb2
clean::
	rm -f $(foreach file,$(ASRC:.tex=) $(ASRC:.rst=),$(addprefix $(file)., $(cleanexts))) $(MISCTRASH) *~
	rm -f comment.cut
	rm -f revision.tex texput.log
	rm -f $(CODE_TEX) code.sty $(CODE:.py=-snippet*.*)


.PHONY: figures
