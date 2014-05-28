import os

srcdirpath = os.path.abspath('./tohosen_pdf')
destdirpath = os.path.abspath('./tohosen_text')

BASE_URL = 'http://www.city.sapporo.jp/st/subway/route_time/documents/{filename}'
stations = [
    ['1', 'h26_01sakaemati_daiya.pdf', '栄町', 'さかえまち'],
    ['2', 'h26_02sindouhigasi_daiya.pdf', '', ''],
    ['3', 'h26_03motomati_daiya.pdf', '', ''],
    ['4', 'h26_04kanzyoudourihigasi_daiya.pdf', '', ''],
    ['5', 'h26_05higasikuyakusyo_daiya.pdf', '', ''],
    ['6', 'h26_06kita13zyouhigasi_daiya.pdf', '', ''],
    ['7', 'h26-01sapporo_daiay.pdf', '', ''],
    ['8', 'h26-01oodori_daiya.pdf', '', ''],
    ['9', 'h26-01housui_daiya.pdf', '', ''],
    ['10', 'h26-01gakuenmae_daiya.pdf', '', ''],
    ['11', 'h26-01toyohirakoen_daiya.pdf', '', ''],
    ['12', 'h26-01misono_daiya.pdf', '', ''],
    ['13', 'h26-01tukisamu_daiya.pdf', '', ''],
    ['14', 'h26-01hukuzumi_daiya.pdf', '', '']
]
