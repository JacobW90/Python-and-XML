import os
import sys
import xml.etree.ElementTree as ET
#from subprocess import call
import subprocess
import glob
from zipfile import ZipFile
#import libxslt
#import libxml2
#from lxml import etree
#import lxml
# etree


counter = 0
file_paths = []


def email():

    print("Enter in the email you'd like to send the Zip File to")
    emal = input()
    c = "mutt -s ""Sources"" -a /home/jwatson4/CS/csc344/sources.zip -- "+emal+" < /home/jwatson4/CS/csc344/sources.zip"
    os.system(c)


def zipit(file_paths2):
    os.chdir("/home/jwatson4/CS/csc344/")
    with ZipFile('sources.zip', 'w') as zip:
        # writing each file one by one
        for file in file_paths2:
            zip.write(file)


def html():
    f = open('/home/jwatson4/CS/csc344/index.html', 'w')

    message = """<html>
    <head></head>
    <a href="./a1/summary_a2.xml">assignment 1 link</a>
    <br />
    <a href="./a2/summary_a1.xml">assignment 2 link</a>
    <br />
    <a href="./a3/summary_a3.xml">assignment 3 link</a>
    <br />
    <a href="./a4/summary_a4.xml">assignment 4 link</a>
    <br />
    <a href="./a5/summary_a0.xml">assignment 5 link</a>
    <body></body>
    </html>"""

    f.write(message)
    f.close()


def xmlboi(name, ra, ls, counter1, ident, item):
    broute = ra.split("/")
    troute = broute[0] + "/" + broute[1] + "/" + broute[2] + "/" + broute[3] + "/" + broute[4] + "/" + broute[5] + "/"
    os.chdir(troute)
    f = open("summary_a" + str(counter1) + ".xml", 'w')

    file = ET.Element('file')
    fake_root = ET.Element(None)
    pi = ET.PI("xml-stylesheet", "type='text/xsl' href='template.xslt'")
    pi.tail = "\n"
    fake_root.append(pi)
    fake_root.append(file)
    ET.SubElement(file, "file").text = str(name)
    ET.SubElement(file, "relative").text = ("./" + item)
    ET.SubElement(file, "line").text = str(ls)
    ET.SubElement(file, "identifiers").text = str(ident)

    (ET.ElementTree(element=fake_root)).write("summary_a" + str(counter1) + ".xml")
    f.close()


def xsl(hath):
    route = hath.split("/")
    proute = route[0] + "/" + route[1] + "/" + route[2] + "/" + route[3] + "/" + route[4] + "/" + route[5] + "/"
    os.chdir(proute)
    f = open("template.xslt", 'w')

    message = """<?xml version="1.0" encoding="UTF-8"?>
    
    <xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
 
  <body>
  <h2>XML Files nice</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th>File Name</th>
      <th>Relative Address</th>
      <th>Line Count</th>
      <th>Identifiers</th>
    </tr>
    <xsl:for-each select="file">
    
    <tr>
      <td><xsl:value-of select="file"/></td>
      <td><a href="{relative}"><xsl:value-of select="relative"/></a></td>
      <td><xsl:value-of select="line"/></td>
      <td><xsl:value-of select="identifiers"/></td>
    </tr>
    </xsl:for-each>
  </table>
  </body>
  </html>
</xsl:template>

</xsl:stylesheet>"""
    f.write(message)
    f.close()


def older(directory1, files1):
    global counter

    hit = 0
    identifiers = ""
    for listItems in files1:
        path = directory1 + "/" + listItems

        if os.path.isfile(path):
            with open(path) as openfile:
                for line in openfile:
                    for part in line.split():
                        if counter > 0:
                            if hit == 1:
                                parts = part.split(";")
                                parts1 = parts[0].split("(")
                                parts2 = parts1[0].split("=")
                                parts3 = parts2[0].split("[")
                                parts4 = parts3[0].split(":")
                                if parts4[0] not in identifiers:
                                    identifiers = identifiers + "," + parts4[0]
                                #print(part)
                                hit = 0
                            if hit == 2:
                                if part not in identifiers:
                                    identifiers = part + ", " + identifiers
                                hit = 0
                            if hit == 3:
                                if "class" in part:
                                    hit = 4
                                elif ":" in part:
                                    parts = part.split(":")
                                    parts1 = parts[0].split("(")
                                    if parts1[0] not in identifiers:
                                        identifiers = parts1[0] + ", " + identifiers
                                    hit = 0
                                else:
                                    hit = 4
                            if hit == 4:
                                if "(" in part:
                                        parts = part.split("(")
                                        if parts[0] not in identifiers:
                                            identifiers = parts[0] + "," + identifiers

                                hit = 0

                            if hit == 0:
                                hit = 0

                                if hit == 5:
                                    if tart not in identifiers:
                                        identifiers = tart + ", " + identifiers
                                    hit = 0
                                elif "int" == part:
                                    hit = 1
                                elif "char" == part:
                                    hit = 1
                                elif "void" == part:
                                    hit = 1
                                elif "Node*" == part:
                                    hit = 1
                                elif ":-" in part:
                                    parts = part.split("(")
                                    if parts[0] not in identifiers:
                                        identifiers = parts[0] + "  " + identifiers
                                elif ")." in part:
                                    if "(" in part:
                                        parts = part.split("(")
                                        if parts[0] not in identifiers:
                                            identifiers = parts[0] + " " + identifiers
                                elif "(defn" in part:
                                    hit = 2
                                elif "var" in part:
                                    hit = 1
                                elif "case" in part:
                                    hit = 3
                                elif "class" in part:
                                    hit = 4
                                elif "def" in part:
                                    hit = 3
                                elif "def" in part:
                                    hit = 4
                        else:
                            if hit == 1:
                                parts = part.split(";")
                                parts1 = parts[0].split("(")
                                parts2 = parts1[0].split("=")
                                parts3 = parts2[0].split("[")
                                parts4 = parts3[0].split(":")
                                if parts4[0] not in identifiers:
                                    identifiers = identifiers + "," + parts4[0]
                                #print(part)
                                hit = 0
                            if hit == 5:
                                carts = cart.split(";")
                                carts1 = carts[0].split("(")
                                carts2 = carts1[0].split("=")
                                carts3 = carts2[0].split("[")
                                carts4 = carts3[0].split(":")
                                carts5 = carts4[0].split(")")
                                if carts5[0] not in identifiers:
                                    identifiers = carts5[0] + ", " + identifiers
                                hit = 0
                            if "=" is part:
                                if counter is 0:
                                    hit = 5
                                    cart = tart
                            elif "for" is part:
                                if counter is 0:
                                    hit = 1
                            elif "in" is part:
                                if counter is 0:
                                    hit = 1
                        tart = part


            stdout = subprocess.run(["wc", "-l", path], stdout=subprocess.PIPE, universal_newlines=True) .stdout.strip()
            print(stdout)
            xmlboi(listItems, path, stdout.split(" ")[0], counter, identifiers, listItems)
            xsl(path)
            counter = counter + 1
        elif os.path.isdir(path):
            older(path, os.listdir(path))


def newer(directory1, files1):
    global file_paths
    for listItems in files1:
        path = directory1 + "/" + listItems

        if os.path.isfile(path):
            file_paths.append(path)
        elif os.path.isdir(path):
            newer(path, os.listdir(path))


directory = sys.argv[1]
files = os.listdir(directory)
older(directory, files)
html()
files = os.listdir(directory)
newer(directory, files)
zipit(file_paths)
email()






