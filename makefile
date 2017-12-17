#CC=python2.7
CC=jython
ADDR=localhost:8080
ARGS=-url "http://$(ADDR)/index.php"

RES_SEQ=test_seq.res
RES_PAR=test_par.res

default: test_par#test_seq

start_php:
	(php -S $(ADDR) &)

test_par: start_php
	echo "**** $@: debut ****" > $(RES_PAR)
	date >> $(RES_PAR)
	echo "-------------------------------------" >> $(RES_PAR)
	$(CC) xcrawler_par.py $(ARGS) >> $(RES_PAR)
	ps -f | grep [p]hp | awk '{print $$2}' | xargs kill -9
	echo "-------------------------------------" >> $(RES_PAR)
	echo "**** $@: fin ****" >> $(RES_PAR)
	date >> $(RES_PAR)

test_seq: start_php
	echo "**** $@: debut ****" > $(RES_SEQ)
	date >> $(RES_SEQ)
	echo "-------------------------------------" >> $(RES_SEQ)
	$(CC) xcrawler_seq.py $(ARGS) >> $(RES_SEQ)
	ps -f | grep [p]hp | awk '{print $$2}' | xargs kill -9
	echo "-------------------------------------" >> $(RES_SEQ)
	echo "**** $@: fin ****" >> $(RES_SEQ)
	date >> $(RES_SEQ)

clean:
	rm *.pyc
	rm *.res
	rm *.class
