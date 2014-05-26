#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from config import filenames, destdirpath

RE_NORMAL1 = re.compile(r"^.*?Holidays(.*?)[^0-9\s].*?Holidays(.*?)Last.*$")
RE_NORMAL2 = re.compile(r"^.*?Holidays(.*?)Last.*?(?:Holidays(.*?)For.*)?$")

def get_text(path):
    with open(path) as f:
        return ''.join(f.readlines())

def get_text_per_direction(text):
    m = RE_NORMAL1.search(text)
    if m:
        return list(m.groups())

    m = RE_NORMAL2.search(text)
    if m:
        dirs = list(m.groups())
        if dirs[1] is None:
            dirs.pop(1)
            if 'For Fukuzumi' in text:
                dirs.append(None)
            else:
                dirs.insert(0, None)
        return dirs

    raise Exception('(((?_?)))')


def parse(text, filename):
    text = text.strip()

    def _parse(res, text, i, nh):
        text_len = len(text)
        h = int(text[i:i+len(str(nh))])
        if h != nh:
            raise Exception('!! hour ',h,'',nh,'',i)
        i += len(str(h))
        res[h] = []

        pm = -1
        while True:
            m = int(text[i:i+2])
            if m >= 60 or m <= pm:
                break
            i += 2
            pm = m
            res[h].append(m)
            if i==text_len:
                break

        return i

    weekdays = {}
    holidays = {}
    i = 0
    if 'sapporo' in filename or 'oodori' in filename \
        or 'housui' in filename or 'gakuen' in filename \
        or 'tukisamu' in filename or 'hukuzumi' in filename \
        or 'toyohira' in filename or 'misono' in filename:
        hours = [6,7,8,8,9,10,11,12,13,14,15,15,16,17,18,19,19,20,21,22,23,0]
        #pdfの取得処理のせいだとは思うが、なぜか8,15,19,24が2回出現する・・・
    else:
        hours = list(range(6, 24)) + [0]

    for nh in hours:
        i = _parse(weekdays, text, i, nh)
        i = _parse(holidays, text, i, nh)

    return weekdays,holidays

def main():
    dias = {}
    for filename in filenames:
        dias[filename] = [None, None]
        path = os.path.join(destdirpath, filename + '.txt')
        text = get_text(path)
        dirs = get_text_per_direction(text)
        for i,v in enumerate(dirs):
            if v is None:
                continue
            dias[filename][i] = parse(v, filename)
    print(dias['h26_01sakaemati_daiya.pdf'][0][0])
    print(dias['h26_01sakaemati_daiya.pdf'][0][1])
    print(dias['h26_01sakaemati_daiya.pdf'][1])


if __name__ == '__main__':
    main()

