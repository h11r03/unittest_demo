import unittest  # Python標準のテストライブラリ
from unittest.mock import patch  # モックオブジェクトを作るための機能
import requests  # 外部APIと通信するためのライブラリ


# 郵便番号から住所を取得するクラス
class ZipCodeSearcher:
    def __init__(self, base_url="https://zipcloud.ibsnet.co.jp/api/search"):
        # APIのURLを初期化
        self.base_url = base_url

    # 郵便番号を受け取って住所情報を返すメソッド
    def search(self, zipcode):
        # APIに渡すURLを作成
        url = f"{self.base_url}?zipcode={zipcode}"
        # APIにリクエストを送信し、レスポンスを受け取る
        response = requests.get(url)
        # エラーが起きた場合は例外を発生させる
        response.raise_for_status()
        # レスポンスをJSON形式に変換して返す
        return response.json()


# テストケースを記述するクラス (unittest.TestCaseを継承)
class TestZipCodeSearcher(unittest.TestCase):
    # 各テストメソッド実行前に呼ばれる初期化処理
    def setUp(self):
        # テスト対象のZipCodeSearcherクラスのインスタンスを作成
        self.searcher = ZipCodeSearcher()

    # モックオブジェクトを使用してAPI呼び出しを模倣するテストケース
    @patch('requests.get')  # requests.get関数をモックに置き換える
    def test_search_success_mock(self, mock_get):  # mock_getはモックオブジェクト
        # モックオブジェクトの戻り値を設定 (APIからの成功レスポンスを模倣)
        mock_get.return_value.status_code = 200  # ステータスコード200を設定
        mock_get.return_value.json.return_value = {  # ダミーの住所データを返すように設定
            "results": [
                {
                    "address1": "東京都",
                    "address2": "千代田区",
                    "address3": "千代田",
                    "zipcode": "1000001",
                }
            ]
        }
        # 実際のAPI呼び出しは行われず、モックの戻り値が使われる
        result = self.searcher.search("1000001")
        # 期待する結果と比較
        self.assertEqual(result['results'][0]['address1'], "東京都")

    # 実際のAPI呼び出しを行うテストケース (モックオブジェクト未使用)
    def test_search_success_real(self):
        # 実際のAPIにリクエストを送信
        result = self.searcher.search("1000001")
        # 期待する結果と比較
        self.assertEqual(result['results'][0]['address1'], "東京都")

# このスクリプトを直接実行したときにテストを実行する記述
if __name__ == '__main__':
    unittest.main()