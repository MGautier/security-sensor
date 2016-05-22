all: pdfmulti

pdfmulti: securityproject.tex
	pdflatex securityproject.tex
	pdflatex securityproject.tex
	pdflatex securityproject.tex

pdf: securityproject.tex
	pdflatex securityproject.tex

show: securityproject.pdf
	evince securityproject.pdf &

clean:
	rm *.log *.lot *.out *.toc *.lof *.aux
