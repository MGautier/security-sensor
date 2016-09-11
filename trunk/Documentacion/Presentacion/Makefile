all: pdfmulti

pdfmulti: Security-Sensor-Slides.tex
	pdflatex Security-Sensor-Slides.tex
	pdflatex Security-Sensor-Slides.tex
	pdflatex Security-Sensor-Slides.tex

show: Security-Sensor-Slides.pdf
	evince Security-Sensor-Slides.pdf &

clean:
	rm *.aux *.log *.nav *.out *.snm *.toc *~
