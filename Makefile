all: svg ps

svg: test.classes.svg test.states.svg test2.states.svg

ps: test.classes.ps test.states.ps test2.states.ps

clean:
	rm -f *.svg *.ps

%.classes.dot: %.classes classes2dot
	./classes2dot $< >$@

%.dep.dot: %.dep ../depends/dep2dot
	../depends/dep2dot $< >$@

%.states.dot: %.states states2dot
	./states2dot $< >$@

%.svg: %.dot setlinewidth.xslt
	dot -Tsvg $< |xsltproc --novalid --stringparam default_stroke_width 0.25 -o $@ setlinewidth.xslt -

%.ps: %.dot
	dot -Tps -Gpage=8.26,11.69 $< |sed 's/^1\( setlinewidth\)/0.25\1/g' >$@
