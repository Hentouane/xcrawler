#CC=python2.7
CC=jython
ADDR=localhost:8080
ARGS=-url "http://$(ADDR)/tests/index.php" -query "query" -v "hentouane" -nbt 4

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
	echo "-------------------------------------" >> $(RES_PAR)
	echo "**** $@: fin ****" >> $(RES_PAR)
	date >> $(RES_PAR)

test_seq: start_php
	echo "**** $@: debut ****" > $(RES_SEQ)
	date >> $(RES_SEQ)
	echo "-------------------------------------" >> $(RES_SEQ)
	$(CC) xcrawler_seq.py $(ARGS) >> $(RES_SEQ)
	echo "-------------------------------------" >> $(RES_SEQ)
	echo "**** $@: fin ****" >> $(RES_SEQ)
	date >> $(RES_SEQ)

tests: start_php test_seq test_par	
	ps -f | grep [p]hp | awk '{print $$2}' | xargs kill -9

clean:
	rm *.pyc
	rm *.res
	rm *.class
