# -*- coding: utf-8 -*-
"""CSVファイルの読み込み処理
"""
import codecs
import csv


def read_from_file(fin, is_firstline_title=True, encoding='shift_jis'):
    if is_firstline_title == False:
        raise Exception("Does not support for is_firstline_title=False."
                        "Please add title line at first.")

    if fin.encoding != encoding:
        fin = codecs.getreader(encoding)(fin.detach())
    items = []
    rows = csv.DictReader(fin, dialect=csv.excel(), quotechar='"', restkey="rest")
    for row in rows:
        rowdict = {}
        for k,v in row.items():
            rowdict[k.strip()] = v.strip()
        items.append(rowdict)
    return items

def read_from_csvfilepath(filename, is_firstline_title=True, encoding='shift_jis'):
    """
    :return rows: csv.DictReaderを返す
    """
    with open(filename, 'r', encoding=encoding) as fin:
        return read_from_file(fin, is_firstline_title)

