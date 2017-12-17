from xml.dom.minidom import *
import sys

fname = "namelist.txt"
fpass = "john.txt"

SIZE = int(sys.argv[1])

def populate_xml(filename, nodename, size, parentnode, doc):
    with open(filename) as f:
        content = f.readlines()

    count = 1
    for name in content:
        if count > size:
            return
        node = doc.createElement(nodename)
        nodetext = doc.createTextNode(name.strip())
        node.appendChild(nodetext)
        parentnode.appendChild(node)
        count += 1

doc = Document()
datanode = doc.createElement("data")
doc.appendChild(datanode)
usersnode = doc.createElement("users")
datanode.appendChild(usersnode)
passwordsnode = doc.createElement("passwords")
datanode.appendChild(passwordsnode)

populate_xml(fname, "user", SIZE, usersnode, doc)

populate_xml(fpass, "password", SIZE, passwordsnode, doc)

print doc.toprettyxml()