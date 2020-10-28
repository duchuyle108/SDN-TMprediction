from xml.dom import minidom
import numpy as np
import os

folderpath = "geant-matrices"

dataset = []

for file in os.listdir(folderpath):
    xmldoc = minidom.parse(folderpath + '/' + file)
    itemlist = xmldoc.getElementsByTagName("src")
    data = np.zeros((23,23),dtype=object)
    for src in itemlist:
        srcid = src.attributes["id"].value
        dstlist = src.getElementsByTagName("dst")
        for dst in dstlist:
            dstid = dst.attributes["id"].value
            element = dst.firstChild.nodeValue
            data[int(srcid)-1][int(dstid)-1] = element
    data = data.flatten()
    filename = file.replace('IntraTM-','')
    filename = filename.replace('.xml','')
    data = np.insert(data, 0, filename, axis=0)
    dataset.append(data)

np.savetxt("geant-flat-tms.csv", dataset,fmt='%s',delimiter=',')