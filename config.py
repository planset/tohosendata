import os

srcdirpath = os.path.abspath('./tohosen_pdf')
destdirpath = os.path.abspath('./tohosen_text')

BASE_URL = 'http://www.city.sapporo.jp/st/subway/route_time/documents/{filename}'
filenames = [
    'h26_01sakaemati_daiya.pdf',
    'h26_02sindouhigasi_daiya.pdf',
    'h26_03motomati_daiya.pdf',
    'h26_04kanzyoudourihigasi_daiya.pdf',
    'h26_05higasikuyakusyo_daiya.pdf',
    'h26_06kita13zyouhigasi_daiya.pdf',
    'h26-01sapporo_daiay.pdf',
    'h26-01oodori_daiya.pdf',
    'h26-01housui_daiya.pdf',
    'h26-01gakuenmae_daiya.pdf',
    'h26-01toyohirakoen_daiya.pdf',
    'h26-01misono_daiya.pdf',
    'h26-01tukisamu_daiya.pdf',
    'h26-01hukuzumi_daiya.pdf'
]
