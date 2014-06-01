from enum import Enum
import codecs
import _io

import requests

CONVERT_GEO_URL = 'http://newspat.csis.u-tokyo.ac.jp/geocode-cgi/geocode.cgi?action=start'

class InputKanjiCode(Enum):
    auto = 'auto'   # 自動設定
    sjis = 'sjis'   # シフトJISコード(SJIS)
    jis = 'jis'     # JISコード(JIS)
    euc = 'euc'     # 拡張UNIXコード(EUC)


class OutputKanjiCode(Enum):
    auto = 'auto'   # 入力ファイルと同じ
    sjis = 'sjis'   # シフトJISコード(SJIS)
    jis = 'jis'     # JISコード(JIS)
    euc = 'euc'     # 拡張UNIXコード(EUC)


class ExactLevel(Enum):
    search = 0      # 探す
    city = 4        # 町字以下で探す 
    street = 5      # 丁目以下で探す
    notsearch = 9999   # 探さない


class UTokyoGeocodeConverter(object):
    def __init__(self, url=CONVERT_GEO_URL):
        self.url_base = url

    def _is_available_services(self):
        r = requests.get(self.url_base)
        return r.status_code == 200

    def execute_file(self, fin, fout,
                ncolumn, 
                spat_port=8800,
                input_kanji_code=InputKanjiCode.auto,
                output_kanji_code=OutputKanjiCode.auto,
                reverse_xy=False,
                exact_level=ExactLevel.search,
                fin_encoding='shift_jis',
                fout_encoding='shift_jis'):

        if not self._is_available_services():
            raise Exception('Not available for converting')

        data = {}
        data['action'] = 'input'
        data['spat_host'] = 'newspat.csis.u-tokyo.ac.jp'
        data['spat_port'] = spat_port
        data['ncolumn'] = ncolumn
        data['input_kanji_code'] = input_kanji_code
        data['output_kanji_code'] = output_kanji_code
        data['reverse_xy'] = 1 if reverse_xy else 0
        data['exact_level'] = exact_level
        data['submit'] = u'送信'
        
        if isinstance(fin, _io.TextIOWrapper) and fin.encoding != fin_encoding:
            fin = codecs.getreader(fin_encoding)(fin.detach())
        if isinstance(fout, _io.TextIOWrapper) and fout.encoding != fout_encoding:
            fout = codecs.getwriter(fout_encoding)(fout.detach())

        r = requests.post(self.url_base, data=data, 
                files=dict(file=fin))

        fout.write(r.text)

        return True

    def execute(self, srccsvpath, destcsvpath,
                ncolumn, 
                spat_port=8800,
                input_kanji_code=InputKanjiCode.auto,
                output_kanji_code=OutputKanjiCode.auto,
                reverse_xy=False,
                exact_level=ExactLevel.search):

        with open(srccsvpath, 'rb') as fin, \
                open(destcsvpath, 'w', encoding='shift_jis') as fout:
            return self.execute_file(fin, fout,
                    ncolumn, spat_port,
                    input_kanji_code, output_kanji_code,
                    reverse_xy, exact_level)


spat_port_items = [
    {"8800":"全国街区レベル(経緯度・世界測地系)"},
    {"8900":"全国街区レベル(公共測量座標系・世界測地系)"},
    {"8600":"全国街区レベル(経緯度・旧測地系)"},
    {"8700":"全国街区レベル(公共測量座標系・旧測地系)"},
    {"8651":"数値地図25000地名（経緯度・旧測地系)"},
    {"8652":"駅名(経緯度・世界測地系)"},
    {"8653":"公共施設(経緯度・旧測地系)"},
    {"8801":"北海道 街区レベル(経緯度・世界測地系)"},
    {"8802":"青森県 街区レベル(経緯度・世界測地系)"},
    {"8803":"岩手県 街区レベル(経緯度・世界測地系)"},
    {"8804":"宮城県 街区レベル(経緯度・世界測地系)"},
    {"8805":"秋田県 街区レベル(経緯度・世界測地系)"},
    {"8806":"山形県 街区レベル(経緯度・世界測地系)"},
    {"8807":"福島県 街区レベル(経緯度・世界測地系)"},
    {"8808":"茨城県 街区レベル(経緯度・世界測地系)"},
    {"8809":"栃木県 街区レベル(経緯度・世界測地系)"},
    {"8810":"群馬県 街区レベル(経緯度・世界測地系)"},
    {"8811":"埼玉県 街区レベル(経緯度・世界測地系)"},
    {"8812":"千葉県 街区レベル(経緯度・世界測地系)"},
    {"8813":"東京都 街区レベル(経緯度・世界測地系)"},
    {"8814":"神奈川県 街区レベル(経緯度・世界測地系)"},
    {"8815":"新潟県 街区レベル(経緯度・世界測地系)"},
    {"8816":"富山県 街区レベル(経緯度・世界測地系)"},
    {"8817":"石川県 街区レベル(経緯度・世界測地系)"},
    {"8818":"福井県 街区レベル(経緯度・世界測地系)"},
    {"8819":"山梨県 街区レベル(経緯度・世界測地系)"},
    {"8820":"長野県 街区レベル(経緯度・世界測地系)"},
    {"8821":"岐阜県 街区レベル(経緯度・世界測地系)"},
    {"8822":"静岡県 街区レベル(経緯度・世界測地系)"},
    {"8823":"愛知県 街区レベル(経緯度・世界測地系)"},
    {"8824":"三重県 街区レベル(経緯度・世界測地系)"},
    {"8825":"滋賀県 街区レベル(経緯度・世界測地系)"},
    {"8826":"京都府 街区レベル(経緯度・世界測地系)"},
    {"8827":"大阪府 街区レベル(経緯度・世界測地系)"},
    {"8828":"兵庫県 街区レベル(経緯度・世界測地系)"},
    {"8829":"奈良県 街区レベル(経緯度・世界測地系)"},
    {"8830":"和歌山県 街区レベル(経緯度・世界測地系)"},
    {"8831":"鳥取県 街区レベル(経緯度・世界測地系)"},
    {"8832":"島根県 街区レベル(経緯度・世界測地系)"},
    {"8833":"岡山県 街区レベル(経緯度・世界測地系)"},
    {"8834":"広島県 街区レベル(経緯度・世界測地系)"},
    {"8835":"山口県 街区レベル(経緯度・世界測地系)"},
    {"8836":"徳島県 街区レベル(経緯度・世界測地系)"},
    {"8837":"香川県 街区レベル(経緯度・世界測地系)"},
    {"8838":"愛媛県 街区レベル(経緯度・世界測地系)"},
    {"8839":"高知県 街区レベル(経緯度・世界測地系)"},
    {"8840":"福岡県 街区レベル(経緯度・世界測地系)"},
    {"8841":"佐賀県 街区レベル(経緯度・世界測地系)"},
    {"8842":"長崎県 街区レベル(経緯度・世界測地系)"},
    {"8843":"熊本県 街区レベル(経緯度・世界測地系)"},
    {"8844":"大分県 街区レベル(経緯度・世界測地系)"},
    {"8845":"宮崎県 街区レベル(経緯度・世界測地系)"},
    {"8846":"鹿児島県 街区レベル(経緯度・世界測地系)"},
    {"8847":"沖縄県 街区レベル(経緯度・世界測地系)"},
    {"8851":"全国 丁目・街区レベル(経緯度・世界測地系)"},
    {"8901":"北海道 街区レベル(公共測量座標系・世界測地系)"},
    {"8902":"青森県 街区レベル(公共測量座標系・世界測地系)"},
    {"8903":"岩手県 街区レベル(公共測量座標系・世界測地系)"},
    {"8904":"宮城県 街区レベル(公共測量座標系・世界測地系)"},
    {"8905":"秋田県 街区レベル(公共測量座標系・世界測地系)"},
    {"8906":"山形県 街区レベル(公共測量座標系・世界測地系)"},
    {"8907":"福島県 街区レベル(公共測量座標系・世界測地系)"},
    {"8908":"茨城県 街区レベル(公共測量座標系・世界測地系)"},
    {"8909":"栃木県 街区レベル(公共測量座標系・世界測地系)"},
    {"8910":"群馬県 街区レベル(公共測量座標系・世界測地系)"},
    {"8911":"埼玉県 街区レベル(公共測量座標系・世界測地系)"},
    {"8912":"千葉県 街区レベル(公共測量座標系・世界測地系)"},
    {"8913":"東京都 街区レベル(公共測量座標系・世界測地系)"},
    {"8914":"神奈川県 街区レベル(公共測量座標系・世界測地系)"},
    {"8915":"新潟県 街区レベル(公共測量座標系・世界測地系)"},
    {"8916":"富山県 街区レベル(公共測量座標系・世界測地系)"},
    {"8917":"石川県 街区レベル(公共測量座標系・世界測地系)"},
    {"8918":"福井県 街区レベル(公共測量座標系・世界測地系)"},
    {"8919":"山梨県 街区レベル(公共測量座標系・世界測地系)"},
    {"8920":"長野県 街区レベル(公共測量座標系・世界測地系)"},
    {"8921":"岐阜県 街区レベル(公共測量座標系・世界測地系)"},
    {"8922":"静岡県 街区レベル(公共測量座標系・世界測地系)"},
    {"8923":"愛知県 街区レベル(公共測量座標系・世界測地系)"},
    {"8924":"三重県 街区レベル(公共測量座標系・世界測地系)"},
    {"8925":"滋賀県 街区レベル(公共測量座標系・世界測地系)"},
    {"8926":"京都府 街区レベル(公共測量座標系・世界測地系)"},
    {"8927":"大阪府 街区レベル(公共測量座標系・世界測地系)"},
    {"8928":"兵庫県 街区レベル(公共測量座標系・世界測地系)"},
    {"8929":"奈良県 街区レベル(公共測量座標系・世界測地系)"},
    {"8930":"和歌山県 街区レベル(公共測量座標系・世界測地系)"},
    {"8931":"鳥取県 街区レベル(公共測量座標系・世界測地系)"},
    {"8932":"島根県 街区レベル(公共測量座標系・世界測地系)"},
    {"8933":"岡山県 街区レベル(公共測量座標系・世界測地系)"},
    {"8934":"広島県 街区レベル(公共測量座標系・世界測地系)"},
    {"8935":"山口県 街区レベル(公共測量座標系・世界測地系)"},
    {"8936":"徳島県 街区レベル(公共測量座標系・世界測地系)"},
    {"8937":"香川県 街区レベル(公共測量座標系・世界測地系)"},
    {"8938":"愛媛県 街区レベル(公共測量座標系・世界測地系)"},
    {"8939":"高知県 街区レベル(公共測量座標系・世界測地系)"},
    {"8940":"福岡県 街区レベル(公共測量座標系・世界測地系)"},
    {"8941":"佐賀県 街区レベル(公共測量座標系・世界測地系)"},
    {"8942":"長崎県 街区レベル(公共測量座標系・世界測地系)"},
    {"8943":"熊本県 街区レベル(公共測量座標系・世界測地系)"},
    {"8944":"大分県 街区レベル(公共測量座標系・世界測地系)"},
    {"8945":"宮崎県 街区レベル(公共測量座標系・世界測地系)"},
    {"8946":"鹿児島県 街区レベル(公共測量座標系・世界測地系)"},
    {"8947":"沖縄県 街区レベル(公共測量座標系・世界測地系)"},
    {"8601":"北海道 街区レベル(経緯度・旧測地系)"},
    {"8602":"青森県 街区レベル(経緯度・旧測地系)"},
    {"8603":"岩手県 街区レベル(経緯度・旧測地系)"},
    {"8604":"宮城県 街区レベル(経緯度・旧測地系)"},
    {"8605":"秋田県 街区レベル(経緯度・旧測地系)"},
    {"8606":"山形県 街区レベル(経緯度・旧測地系)"},
    {"8607":"福島県 街区レベル(経緯度・旧測地系)"},
    {"8608":"茨城県 街区レベル(経緯度・旧測地系)"},
    {"8609":"栃木県 街区レベル(経緯度・旧測地系)"},
    {"8610":"群馬県 街区レベル(経緯度・旧測地系)"},
    {"8611":"埼玉県 街区レベル(経緯度・旧測地系)"},
    {"8612":"千葉県 街区レベル(経緯度・旧測地系)"},
    {"8613":"東京都 街区レベル(経緯度・旧測地系)"},
    {"8614":"神奈川県 街区レベル(経緯度・旧測地系)"},
    {"8615":"新潟県 街区レベル(経緯度・旧測地系)"},
    {"8616":"富山県 街区レベル(経緯度・旧測地系)"},
    {"8617":"石川県 街区レベル(経緯度・旧測地系)"},
    {"8618":"福井県 街区レベル(経緯度・旧測地系)"},
    {"8619":"山梨県 街区レベル(経緯度・旧測地系)"},
    {"8620":"長野県 街区レベル(経緯度・旧測地系)"},
    {"8621":"岐阜県 街区レベル(経緯度・旧測地系)"},
    {"8622":"静岡県 街区レベル(経緯度・旧測地系)"},
    {"8623":"愛知県 街区レベル(経緯度・旧測地系)"},
    {"8624":"三重県 街区レベル(経緯度・旧測地系)"},
    {"8625":"滋賀県 街区レベル(経緯度・旧測地系)"},
    {"8626":"京都府 街区レベル(経緯度・旧測地系)"},
    {"8627":"大阪府 街区レベル(経緯度・旧測地系)"},
    {"8628":"兵庫県 街区レベル(経緯度・旧測地系)"},
    {"8629":"奈良県 街区レベル(経緯度・旧測地系)"},
    {"8630":"和歌山県 街区レベル(経緯度・旧測地系)"},
    {"8631":"鳥取県 街区レベル(経緯度・旧測地系)"},
    {"8632":"島根県 街区レベル(経緯度・旧測地系)"},
    {"8633":"岡山県 街区レベル(経緯度・旧測地系)"},
    {"8634":"広島県 街区レベル(経緯度・旧測地系)"},
    {"8635":"山口県 街区レベル(経緯度・旧測地系)"},
    {"8636":"徳島県 街区レベル(経緯度・旧測地系)"},
    {"8637":"香川県 街区レベル(経緯度・旧測地系)"},
    {"8638":"愛媛県 街区レベル(経緯度・旧測地系)"},
    {"8639":"高知県 街区レベル(経緯度・旧測地系)"},
    {"8640":"福岡県 街区レベル(経緯度・旧測地系)"},
    {"8641":"佐賀県 街区レベル(経緯度・旧測地系)"},
    {"8642":"長崎県 街区レベル(経緯度・旧測地系)"},
    {"8643":"熊本県 街区レベル(経緯度・旧測地系)"},
    {"8644":"大分県 街区レベル(経緯度・旧測地系)"},
    {"8645":"宮崎県 街区レベル(経緯度・旧測地系)"},
    {"8646":"鹿児島県 街区レベル(経緯度・旧測地系)"},
    {"8647":"沖縄県 街区レベル(経緯度・旧測地系)"},
    {"8701":"北海道 街区レベル(公共測量座標系・旧測地系)"},
    {"8702":"青森県 街区レベル(公共測量座標系・旧測地系)"},
    {"8703":"岩手県 街区レベル(公共測量座標系・旧測地系)"},
    {"8704":"宮城県 街区レベル(公共測量座標系・旧測地系)"},
    {"8705":"秋田県 街区レベル(公共測量座標系・旧測地系)"},
    {"8706":"山形県 街区レベル(公共測量座標系・旧測地系)"},
    {"8707":"福島県 街区レベル(公共測量座標系・旧測地系)"},
    {"8708":"茨城県 街区レベル(公共測量座標系・旧測地系)"},
    {"8709":"栃木県 街区レベル(公共測量座標系・旧測地系)"},
    {"8710":"群馬県 街区レベル(公共測量座標系・旧測地系)"},
    {"8711":"埼玉県 街区レベル(公共測量座標系・旧測地系)"},
    {"8712":"千葉県 街区レベル(公共測量座標系・旧測地系)"},
    {"8713":"東京都 街区レベル(公共測量座標系・旧測地系)"},
    {"8714":"神奈川県 街区レベル(公共測量座標系・旧測地系)"},
    {"8715":"新潟県 街区レベル(公共測量座標系・旧測地系)"},
    {"8716":"富山県 街区レベル(公共測量座標系・旧測地系)"},
    {"8717":"石川県 街区レベル(公共測量座標系・旧測地系)"},
    {"8718":"福井県 街区レベル(公共測量座標系・旧測地系)"},
    {"8719":"山梨県 街区レベル(公共測量座標系・旧測地系)"},
    {"8720":"長野県 街区レベル(公共測量座標系・旧測地系)"},
    {"8721":"岐阜県 街区レベル(公共測量座標系・旧測地系)"},
    {"8722":"静岡県 街区レベル(公共測量座標系・旧測地系)"},
    {"8723":"愛知県 街区レベル(公共測量座標系・旧測地系)"},
    {"8724":"三重県 街区レベル(公共測量座標系・旧測地系)"},
    {"8725":"滋賀県 街区レベル(公共測量座標系・旧測地系)"},
    {"8726":"京都府 街区レベル(公共測量座標系・旧測地系)"},
    {"8727":"大阪府 街区レベル(公共測量座標系・旧測地系)"},
    {"8728":"兵庫県 街区レベル(公共測量座標系・旧測地系)"},
    {"8729":"奈良県 街区レベル(公共測量座標系・旧測地系)"},
    {"8730":"和歌山県 街区レベル(公共測量座標系・旧測地系)"},
    {"8731":"鳥取県 街区レベル(公共測量座標系・旧測地系)"},
    {"8732":"島根県 街区レベル(公共測量座標系・旧測地系)"},
    {"8733":"岡山県 街区レベル(公共測量座標系・旧測地系)"},
    {"8734":"広島県 街区レベル(公共測量座標系・旧測地系)"},
    {"8735":"山口県 街区レベル(公共測量座標系・旧測地系)"},
    {"8736":"徳島県 街区レベル(公共測量座標系・旧測地系)"},
    {"8737":"香川県 街区レベル(公共測量座標系・旧測地系)"},
    {"8738":"愛媛県 街区レベル(公共測量座標系・旧測地系)"},
    {"8739":"高知県 街区レベル(公共測量座標系・旧測地系)"},
    {"8740":"福岡県 街区レベル(公共測量座標系・旧測地系)"},
    {"8741":"佐賀県 街区レベル(公共測量座標系・旧測地系)"},
    {"8742":"長崎県 街区レベル(公共測量座標系・旧測地系)"},
    {"8743":"熊本県 街区レベル(公共測量座標系・旧測地系)"},
    {"8744":"大分県 街区レベル(公共測量座標系・旧測地系)"},
    {"8745":"宮崎県 街区レベル(公共測量座標系・旧測地系)"},
    {"8746":"鹿児島県 街区レベル(公共測量座標系・旧測地系)"},
    {"8747":"沖縄県 街区レベル(公共測量座標系・旧測地系)"},
    {"8852":"[試験中]全国 住居表示レベル(経緯度・世界測地系)"},
]
