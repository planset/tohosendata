#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import codecs
import _io

import csvutil


def convert_from_filepath_to_filepath(srccsvpath, jsonpath):
    """CSVを読み込んでJSONにして保存

    >>> convert_from_filepath_to_filepath('station_with_geo.csv', 'station.json')
    """
    data = csvutil.read_from_csvfilepath(srccsvpath)
    with open(jsonpath, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data))

def convert_from_stdin_to_stdout():
    """STDINからCSV文字列を読み込んでJSONに変換してSTDOUTに出力

    sample::
    
        cat station_with_geo.csv| python csv2json.py
    """
    fin = sys.stdin
    fout = sys.stdout
    encoding = 'utf-8'
    data = csvutil.read_from_file(fin)
    if isinstance(fout, _io.TextIOWrapper) and fout.encoding != encoding:
        fout = codecs.getwriter(encoding)(fout.detach())
    fout.write(json.dumps(data))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="calculate X to the power of Y")

    parser.add_argument("srccsvpath", type=str, help="The source CSV file path.", default=None, nargs='?')
    parser.add_argument("savejsonpath", type=str, help="The destination JSON file path.", default=None, nargs='?')

    args = parser.parse_args()
    if args.srccsvpath and args.savejsonpath:
        convert_from_filepath_to_filepath(args.srccsvpath, args.savejsonpath)
    else:
        convert_from_stdin_to_stdout()


