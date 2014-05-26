#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import PyPDF2

from config import srcdirpath, destdirpath


def get_pdf_text(path):
    """PDFファイルからテキスト情報を抜き出す"""
    text = ""
    pdf = PyPDF2.PdfFileReader(open(path, "rb"))
    for i in range(0, pdf.getNumPages()):
        text += pdf.getPage(i).extractText() + "\n"
    text = " ".join(text.replace(u"\xa0", " ").strip().split())
    return text

def pdf2text(srcdirpath, destdirpath):
    """srcdirpathに含まれるpdfファイルのテキスト情報を、
    destdirpathに出力する"""
    if not os.path.exists(destdirpath):
        os.mkdir(destdirpath)

    for filename in os.listdir(srcdirpath):
        if filename.split('.')[-1] != 'pdf':
            continue

        srcfilepath = os.path.join(srcdirpath, filename)
        destfilepath =  os.path.join(destdirpath, filename + '.txt')

        text = get_pdf_text(srcfilepath)

        with open(destfilepath, 'w') as f:
            f.write(text)

if __name__ == '__main__':
    pdf2text(srcdirpath,  destdirpath)

