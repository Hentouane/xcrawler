from Queue import Queue
import sys
from threading import Thread, Lock
import xcrawler

""" Implementation parallele du XCrawler """


""" Classe Travailleur """
class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            func(*args, **kargs)
            self.tasks.task_done()


""" Classe sac de taches """
class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()


""" Explore le texte d'un noeud """
def crawlText(xcrawler, path, node):
    text_length = xcrawler.find_length(path + "/text()")
    if text_length > 0:
        text = xcrawler.find_name(path + "/text()", text_length)

        text_node = xcrawler.xml.createTextNode(text)
        node.appendChild(text_node)

    return node

""" Explore un noeud et son nom. Cree une tache si le nom a des enfants """
def crawlNode(xcrawler, path, pool, parent_node=None):
    length = xcrawler.find_length("name(" + path + ")")
    name = xcrawler.find_name("name(" + path + ")", length)

    node = xcrawler.xml.createElement(name)
    node = crawlText(xcrawler, path, node)

    if parent_node is None:
        xcrawler.xml.appendChild(node)
    else:
        xcrawler.mutex.acquire()
        try:
            parent_node.appendChild(node)
        finally:
            xcrawler.mutex.release()

    if xcrawler.count_node(path + "/*") > 0:
        pool.add_task(crawlXml, xcrawler, path + "/*", pool, node)

    return node


""" Fonction principale creant des taches pour chacun des enfants du noeud donne """
def crawlXml(xcrawler, base_path, pool, parent_node=None):
    nodeIndex = 1
    path = base_path
    nodeCount = xcrawler.count_node(path)
    while nodeIndex <= nodeCount:
        path = base_path + "[{}]".format(nodeIndex)
        pool.add_task(crawlNode, xcrawler, path, pool, parent_node)

        nodeIndex += 1


def run(xcrawler):
    pool = ThreadPool(xcrawler.nb_thread)

    """ On debute avec le noeud initial/root """
    crawlNode(xcrawler, '/*[1]', pool)

    pool.wait_completion()
    print xcrawler.xml.toprettyxml()


if __name__ == '__main__':
    if len(sys.argv) < 9:
        xcrawler.usage("XCrawler_par")
    else:
        xcrawler = xcrawler.XCrawler()
        xcrawler.mutex = Lock()
        run(xcrawler)
