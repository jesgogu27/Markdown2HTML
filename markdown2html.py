#!/usr/bin/python3
""" script that takes an argument 2 strings  """

if __name__ == '__main__':

    import sys
    from os import path
    import re
    import hashlib

    mkd = {"#": "h1", "##": "h2", "###": "h3", "####": "h4", "#####": "h5", "######": "h6", "-": "ul", "*": "ol"}

    def convert_tittles(options):
        etiq = mkd[lineSplit[0]] 
        writeT = line.replace("{} ".format(lineSplit[0]), "<{}>".format(etiq))
        writeT = writeT[:-1] + ("</{}>\n".format(etiq))
        fw.write(writeT)

    def text_inline(line, options):
        aux = 0
        while options in line:
            if not aux:
                if options == "**":
                    line = line.replace(options, "<b>", 1)
                    aux = 1
                else:
                    line = line.replace(options, "<em>", 1)
                    aux = 1
            else:
                if options == "**":
                    line = line.replace(options, "</b>", 1)
                    aux = 0
                else: 
                    line = line.replace(options, "</em>", 1)
                    aux = 0
        return line

    def create_md(line):
        utx = []
        while "[[" in line and "]]" in line:
            utx = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '[' and line[j + 1] == '[':
                    utx.append(j)
                elif not j == len(line) - 1 and line[j] == "]" and line[j + 1] == ']':
                    utx.append(j)
            if utx:
                sliceObj = slice(utx[0], utx[1] + 2)
            
            aux_utx = line[sliceObj]
            go_hash = aux_utx[2:-2]
            mt = hashlib.md5(go_Hash.encode()).hexdigest()
            line = line.replace(aux_utx, mt)
        return line

    def caseMarkdown(line):
        rep = []
        s = ''
        while '((' in line:
            rep = []
            for j in range(len(line)):
                if not j == len(line) - 1 and line[j] == '(' and line[j + 1] == '(':
                    rep.append(j)
                elif not j == len(line) - 1 and line[j] == ")" and line[j + 1] == ')':
                    rep.append(j)
            if rep:
                sliceObj = slice(rep[0], rep[1] + 2)
            toRep = line[sliceObj]
            s = toRep
            for char in toRep:
                if char == 'c':
                    toRep = toRep.replace('c', '')
                elif char == 'C':
                    toRep = toRep.replace('C', '')
            line = line.replace(s, toRep[2:-2])
        return line 

    with open(sys.argv[1], mode='r') as fr, open(sys.argv[2], mode='w+') as fw:
        first = 0
        f = 0
        read = fr.readlines()
        for i, line in enumerate(read):
            if "**" in line:
                line = text_inline(line, "**")
            if "__" in line:
                line = text_inline(line, "__")
            if "[[" in line and "]]" in line:
                line = create_md(line)
            if "((" in line and "))" in line:
                line = caseMarkdown(line) 
                     
            # split
            lineSplit = line.split(' ')
            if lineSplit[0] in mkd:
                if lineSplit[0].startswith('#'):
                    convert_tittles(lineSplit[0])
                elif lineSplit[0].startswith("-") or lineSplit[0].startswith("*"):
                    tag = mkd[lineSplit[0]]
                    if not first:
                        writeT = "<{}>\n".format(tag)
                        fw.write(writeT)
                        first = lineSplit[0]
                    writeT = line.replace("{} ".format(lineSplit[0]), "<li>")
                    writeT = writeT[:-1] + ("</li>\n")
                    fw.write(writeT)
                    if i is len(read) - 1 or not read[i + 1].startswith("{} ".format(first)):
                        writeT = "</{}>\n".format(tag)
                        fw.write(writeT)
                        first = 0
            else:
                if line[0] != "\n":
                    if not f:
                        fw.write("<p>\n")
                        f = 1
                    fw.write(line)
                    if i != len(read) - 1 and read[i + 1][0] != "\n" and read[i + 1][0] not in mkd:
                        fw.write("<br/>\n")
                    else: 
                        fw.write("</p>\n")
                        f = 0
    exit(0)



    if len(sys.argv) < 3:
        sys.stderr.write('Usage: ./markdown2html.py README.md README.html\n')
        exit(1)
    if not path.exists(sys.argv[1]):
        sys.stderr.write("Missing " + sys.argv[1] + '\n')
        exit(1)
