from Queue import Queue
from threading import Thread
from xcrawler import XCrawler


class Worker(Thread):
    """Thread executing tasks from a given tasks queue"""

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception, e:
                print e
            finally:
                self.tasks.task_done()


class ThreadPool:
    """Pool of threads consuming tasks from a queue"""

    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """Add a task to the queue"""
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """Wait for completion of all the tasks in the queue"""
        self.tasks.join()


NBT = 4


def crawlText(xcrawler, path, node):
    text_length = xcrawler.find_length(path + "/text()")
    if text_length > 0:
        text = xcrawler.find_name(path + "/text()", text_length)
        text_node = xcrawler.xml.createTextNode(text)
        node.appendChild(text_node)

    return node


def crawlNode(xcrawler, path, pool, parent_node=None):
    length = xcrawler.find_length("name(" + path + ")")
    name = xcrawler.find_name("name(" + path + ")", length)
    node = xcrawler.xml.createElement(name)
    node = crawlText(xcrawler, path, node)

    if parent_node is None:
        xcrawler.xml.appendChild(node)
    else:
        parent_node.appendChild(node)

    if xcrawler.count_node(path + "/*") > 0:
        pool.add_task(crawlXml, xcrawler, path + "/*", pool, node)

    return node


#def crawlXmlRange(xcrawler, base_path, parent_node, range):


def crawlXml(xcrawler, base_path, pool, parent_node=None):
    nodeIndex = 1
    path = base_path
    nodeCount = xcrawler.count_node(path)
    while nodeIndex <= nodeCount:
        path = base_path + "[{}]".format(nodeIndex)
        pool.add_task(crawlNode, xcrawler, path, pool, parent_node)

        nodeIndex += 1


def run(xcrawler):
    pool = ThreadPool(20)

    ''' On debute avec le noeud initial/root '''

    crawlNode(xcrawler, '/*[1]', pool)
    pool.wait_completion()
    print xcrawler.xml.toprettyxml()


if __name__ == '__main__':
    xcrawler = XCrawler()
    run(xcrawler)
