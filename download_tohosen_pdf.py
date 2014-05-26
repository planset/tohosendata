#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import urllib.request

from config import BASE_URL, filenames, srcdirpath

if not os.path.exists(srcdirpath):
    os.mkdir(srcdirpath)

for filename in filenames:
    url = BASE_URL.format(filename=filename)
    srcfilepath = os.path.join(srcdirpath, filename)
    urllib.request.urlretrieve(url, srcfilepath)

