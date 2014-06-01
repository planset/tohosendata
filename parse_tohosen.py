#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import json

from config import stations, destdirpath


# 文字列の中から時刻表の部分だけを抜き出すregex
RE_P1 = re.compile(r"^.*?Holidays(.*?)[^0-9\s].*?Holidays(.*?)Last.*$")
RE_P2 = re.compile(r"^.*?Holidays(.*?)Last.*?(?:Holidays(.*?)For.*)?$")


class NotMatchException(Exception): pass

class NotFoundStationException(Exception): pass


def get_text(path):
    with open(path) as f:
        return ''.join(f.readlines())

def get_text_per_direction(text):
    """正規表現で時刻表っぽいところを抽出する
    戻り値はリストで[0]には福住方面行きの時刻表
    [1]には栄町方面行きの時刻表を格納する。
    """
    m = RE_P1.search(text)
    if m:
        return list(m.groups())

    m = RE_P2.search(text)
    if m:
        dirs = list(m.groups())
        if dirs[1] is None:
            dirs.pop(1)
            if 'For Fukuzumi' in text:
                dirs.append(None)
            elif 'For Sakaemachi' in text:
                dirs.insert(0, None)
            else:
                raise NotFoundStationException()
        return dirs

    raise NotMatchException()


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
        #どうにかしたい。extractText周りのパラメータ調整を試してみる、とか。
    else:
        hours = list(range(6, 24)) + [0]

    for nh in hours:
        i = _parse(weekdays, text, i, nh)
        i = _parse(holidays, text, i, nh)

    return weekdays,holidays

def main():
    """
    dia[station_id]に該当する駅の時刻表
    時刻表[0]には平日の時刻表
    時刻表[1]には休日の時刻表
    平日の時刻表[0]に福住方面行きの時刻表
    平日の時刻表[1]に栄町方面行きの時刻表
    休日の時刻表[0]に福住方面行きの時刻表
    休日の時刻表[1]に栄町方面行きの時刻表
    dia.jsonに保存する
    """
    dia = {}
    for station in stations:
        filename = station['pdf_file_name']
        station_id = station['station_id']
        dia[station_id] = [None, None]
        path = os.path.join(destdirpath, filename + '.txt')
        text = get_text(path)
        dirs = get_text_per_direction(text)
        for i,v in enumerate(dirs):
            if v is None:
                continue
            dia[station_id][i] = parse(v, filename)

    with open('dia.json', 'w') as f:
        f.write(json.dumps(dia))


if __name__ == '__main__':
    main()

