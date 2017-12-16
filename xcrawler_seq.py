from xcrawler import XCrawler


def crawlText(xcrawler, path, node):
    text_length = xcrawler.find_length(path + "/text()")
    if text_length > 0:
        text = xcrawler.find_name(path + "/text()", text_length)
        text_node = xcrawler.xml.createTextNode(text)
        node.appendChild(text_node)

    return node


def crawlXml(xcrawler, base_path, parent_node=None):
    nodeIndex = 1
    path = base_path
    nodeCount = xcrawler.count_node(path)
    while nodeIndex <= nodeCount:
        path = base_path + "[{}]".format(nodeIndex)
        length = xcrawler.find_length("name(" + path + ")")
        name = xcrawler.find_name("name(" + path + ")", length)

        node = xcrawler.xml.createElement(name)

        node = crawlText(xcrawler, path, node)

        if parent_node is None:
            xcrawler.xml.appendChild(node)
        else:
            parent_node.appendChild(node)
        if xcrawler.count_node(path + "/*") > 0:
            crawlXml(xcrawler, path + "/*", node)
        nodeIndex += 1


def run(xcrawler):
    crawlXml(xcrawler, '/*')
    print xcrawler.xml.toprettyxml()

if __name__ == '__main__':
    xcrawler = XCrawler()
    run(xcrawler)