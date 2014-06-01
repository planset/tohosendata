#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CSVアドレスマッチングサービスを使って住所から緯度経度を取得する
"""
import sys
import u_tokyo_geocode


def geocoding_filepath(srccsvpath, destcsvpath, ncolumn):
    """
    example::
    
        geocoding.py -n 5 station.csv station_with_geo.csv
    """
    converter = u_tokyo_geocode.UTokyoGeocodeConverter()
    converter.execute(srccsvpath, destcsvpath, ncolumn)


def geocoding_stdin_stdout(ncolumn):
    """
    example::

        cat station.csv | geocoding.py -n 5
    """
    converter = u_tokyo_geocode.UTokyoGeocodeConverter()
    converter.execute_file(sys.stdin, sys.stdout, ncolumn)

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="calculate X to the power of Y")
    parser.add_argument("srccsvpath", type=str, help="The source CSV file path.", default=None, nargs='?')
    parser.add_argument("destcsvpath", type=str, help="The destination CSV file path.", default=None, nargs='?')
    parser.add_argument("ncolumn", type=str, help="The column number of address.", default=None)

    args = parser.parse_args()
    if args.srccsvpath and args.destcsvpath:
        geocoding_filepath(args.srccsvpath, args.destcsvpath, args.ncolumn)
    else:
        geocoding_stdin_stdout(args.ncolumn)


