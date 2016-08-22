all: pdfmulti

pdfmulti: securityproject.tex
	pdflatex securityproject.tex
	bibtex securityproject.aux
	pdflatex securityproject.tex
	pdflatex securityproject.tex

others: first-page second-page auth tutor thanks

first-page: primerahoja.tex
	pdflatex primerahoja.tex

second-page: primerahoja-en.tex
	pdflatex primerahoja-en.tex

auth: autorizacion.tex
	pdflatex autorizacion.tex

tutor: tutor.tex
	pdflatex tutor.tex

thanks: agradecimientos.tex
	pdflatex agradecimientos.tex

pdf: securityproject.tex
	pdflatex securityproject.tex

show: securityproject.pdf
	evince securityproject.pdf &

clean:
	rm *.log *.lot *.out *.toc *.lof *.aux *.bbl *.blg *.dvi
