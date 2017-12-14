CC=python2.7
ADDR=localhost:8080
ARGS=-url "http://$(ADDR)/index.php"

default: test_seq

start_php:
	(php -S $(ADDR) &)

test_seq: start_php
	$(CC) xcrawler.py $(ARGS) > test_seq.res
	ps -f | grep [p]hp | awk '{print $$2}' | xargs kill -9
