import os, sys
import time
from threading import Lock
from xcrawler import XCrawler
import xcrawler_par
import xcrawler_seq

''' Script utilise pour prendre les mesures d'execution du XCrawler '''

URL = "http://localhost:8080/tests/test-{}.php"
QUERY = "query"
SURE_VALUE = "0"
TESTS = [8,16,32]
NBTS = [1,2,4,8]


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    sys.stdout = sys.__stdout__


def print_results(time, size, nbt = "-"):
    print "\t" + str(size) + ":\t" + str(time) + "\t" + str(nbt)


def setup_xcrawler():
    xcrawler = XCrawler()
    xcrawler.query = QUERY
    xcrawler.sure_value = SURE_VALUE

    return xcrawler


if __name__ == '__main__':
    print "Legende"
    print "Taille d'echantillon:\tTemps d'execution\t# Threads\n"
    print "**** Tests sequentiels ****"
    for test in TESTS:
        results = []
        for _ in range(0, 3):
            xcrawler = setup_xcrawler()
            xcrawler.url = URL.format(test)
            start = time.time()
            block_print()
            xcrawler_seq.run(xcrawler)
            enable_print()
            end = time.time()
            results.append(end - start)
        print_results(min(results), test)

    print
    print "**** Tests paralleles ****"
    for test in TESTS:
        for nbt in NBTS:
            results = []
            for _ in range(0, 3):
                xcrawler = setup_xcrawler()
                xcrawler.url = URL.format(test)
                xcrawler.nb_thread = nbt
                xcrawler.mutex = Lock()
                start = time.time()
                block_print()
                xcrawler_par.run(xcrawler)
                enable_print()
                end = time.time()
                results.append(end - start)
            print_results(min(results), test, nbt)

