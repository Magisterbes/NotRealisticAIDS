import numpy as np
import tqdm
import os
import sys

dir = '''C:/GD/Models/nrealisticAIDS/'''


def FillFromFileNoStemm(fname):
    res = []
    strr = ""
    f = open(fname)
    for line in tqdm.tqdm(f):
        if "________________" in line:
            res.append(strr)
            strr =""
        strr +=line.strip()
    f.close()
    return res


def FillFromFileLines(fname):
    res = []
    strr = ""
    f = open(fname)
    for line in tqdm.tqdm(f):
        res.append(line.strip())

    f.close()
    return res


def SaveJustLines(sample, fname,clear = False):

    if clear:
        text_file = open(fname, "w")
        text_file.write("")
        text_file.close()

    text_file = open(fname, "a")
    for txt in sample:
        try:
            text_file.write(txt)
            text_file.write('\n')
        except:
            a=1
    text_file.close()


def GetFilesStartWith(dir, string):
    lst = os.listdir(dir)
    res= []
    for fname in lst:
        if fname.startswith(string):
            res.append(fname)

    return res


def GetDataStartWith(name):
    files = GetFilesStartWith(io.dir,name)

    res = []
    for fname in files:
        data = FillFromFileNoStemm(io.dir + fname)
        for txt in data:
            res.append(txt)
    return res
