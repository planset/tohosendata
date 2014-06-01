======
README
======
札幌市の東豊線時刻表PDFから、使いやすい形のデータを気合で作ります。

station.csvをベースに、緯度経度付きの駅情報ファイルstation.jsonと、出発時刻データのdia.jsonを出力します。


Requirement
===========
* python3
* pip: pypdf2, requests


How to use
==========
::

    pip install -r requirements.txt

    # station.csvを元に緯度経度を取得して駅情報を作成
    cat station.csv | python geocoding.py 5 | python csv2json.py > station.json

    # 東豊線のPDFをダウンロード
    python download_tohosen_pdf.py

    # PDFをテキストに変換
    python pdf2text.py

    # 変換した変なテキストから時刻表っぽいところを抽出
    python parse_tohosen.py

