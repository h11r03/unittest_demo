import json
import os
import time
import unittest
from unittest.mock import patch, mock_open

# ToDoListクラスの定義
class ToDoList:
    def __init__(self, data_file="test_todo.json"):
        """
        ToDoListクラスの初期化メソッド

        Args:
            data_file (str, optional): タスクを保存するJSONファイル名. Defaults to "test_todo.json".
        """
        # タスクを保存するJSONファイル名を設定
        self.data_file = data_file
        # JSONファイルからタスクを読み込む
        self.tasks = self.load_data()

    def load_data(self):
        """
        JSONファイルからタスクデータを読み込むメソッド

        Returns:
            dict: 読み込んだタスクデータ
        """
        try:
            # JSONファイルを開く
            with open(self.data_file, "r") as f:
                data = json.load(f)
                # タイムスタンプをfloatに変換
                for task_list in data.values():
                    for task in task_list:
                        task['timestamp'] = float(task['timestamp'])
                return data
        except FileNotFoundError:
            # ファイルが存在しない場合は空のタスクリストを作成
            return {"active": [], "completed": []}
        except json.JSONDecodeError:
            # JSONファイルが破損している場合は警告メッセージを表示し、空のタスクリストを作成
            print(f"Warning: {self.data_file} is corrupted. Creating a new file.")
            return {"active": [], "completed": []}

    def save_data(self):
        """
        タスクデータをJSONファイルに保存するメソッド
        """
        try:
            # JSONファイルを開く
            with open(self.data_file, "w") as f:
                # タスクデータをJSON形式でファイルに書き込む
                json.dump(self.tasks, f, indent=4)
        except OSError as e:
            # ファイル書き込みエラーの場合、エラーメッセージを表示
            print(f"Error saving data: {e}")

    def add_task(self, task, priority="中"):
        """
        新しいタスクを追加するメソッド

        Args:
            task (str): タスク名
            priority (str, optional): 優先度. Defaults to "中".

        Raises:
            ValueError: タスク名が空の場合
        """
        if task != "":
            # 新しいタスクを作成し、タスクリストに追加
            new_task = {"task": task, "priority": priority, "timestamp": time.time()}
            self.tasks["active"].append(new_task)
            # タスクデータを保存
            self.save_data()
        else:
            # タスク名が空の場合、エラーを発生させる
            raise ValueError("タスクは空にできません。")

    def complete_task(self, index):
        """
        タスクを完了済みへ移動するメソッド

        Args:
            index (int): 完了するタスクのインデックス

        Raises:
            IndexError: 無効なインデックスが指定された場合
        """
        if 0 <= index < len(self.tasks["active"]):
            # 指定されたインデックスのタスクを完了済みリストに移動
            completed_task = self.tasks["active"].pop(index)
            self.tasks["completed"].append(completed_task)
            # タスクデータを保存
            self.save_data()
        else:
            # 無効なインデックスが指定された場合、エラーを発生させる
            raise IndexError("無効なタスクインデックスです。")

    def get_active_tasks(self):
        """
        アクティブなタスクを取得するメソッド

        Returns:
            list: アクティブなタスクのリスト
        """
        return self.tasks["active"]

    def get_completed_tasks(self):
        """
        完了済みのタスクを取得するメソッド

        Returns:
            list: 完了済みのタスクのリスト
        """
        return self.tasks["completed"]

    def set_priority(self, index, priority):
        """
        タスクの優先度を設定するメソッド

        Args:
            index (int): 優先度を変更するタスクのインデックス
            priority (str): 新しい優先度

        Raises:
            ValueError: 無効な優先度が指定された場合
            IndexError: 無効なインデックスが指定された場合
        """
        if priority not in ["高", "中", "低"]:
            raise ValueError("優先度は「高」「中」「低」のいずれかを入力してください。")
        if 0 <= index < len(self.tasks["active"]):
            # 指定されたインデックスのタスクの優先度を変更
            self.tasks["active"][index]["priority"] = priority
            # タスクデータを保存
            self.save_data()
        else:
            # 無効なインデックスが指定された場合、エラーを発生させる
            raise IndexError("無効なタスクインデックスです。")

    def search_tasks(self, keyword):
        """
        キーワードを含むタスクを検索するメソッド

        Args:
            keyword (str): 検索キーワード

        Returns:
            list: キーワードを含むタスクのリスト
        """
        result = []
        for task in self.tasks["active"]:
            # タスク名にキーワードが含まれている場合は結果リストに追加
            if keyword.lower() in task["task"].lower():
                result.append(task)
        return result

    def sort_tasks(self, key, reverse=False):
        """
        タスクをソートするメソッド

        Args:
            key (str): ソートに使用するキー ("priority"または"timestamp")
            reverse (bool, optional): Falseは昇順、Trueは降順. Defaults to False.

        Raises:
            ValueError: 無効なソートキーが指定された場合
        """
        if key not in ["priority", "timestamp"]:
            raise ValueError("ソートキーは 'priority' または 'timestamp' を指定してください。")
        
        if key == "priority":
            # 優先度でソート
            self.tasks["active"] = sorted(self.tasks["active"], key=lambda item: ({"高":0, "中": 1, "低": 2}[item[key]]), reverse=reverse)
        else:
            # タイムスタンプでソート
            self.tasks["active"] = sorted(self.tasks["active"], key=lambda item: item[key], reverse=reverse)
        # タスクデータを保存
        self.save_data()

# ToDoListクラスのテストクラス
class TestToDoListAdvanced(unittest.TestCase):
    def setUp(self):
        """
        テストケース実行前のセットアップ
        """
        # テストデータ
        self.test_data = {
            "active": [
                {"task": "買い物", "priority": "高", "timestamp": 1670476800.0},
                {"task": "掃除", "priority": "低", "timestamp": 1670563200.0},
                {"task": "洗濯", "priority": "中", "timestamp": 1670649600.0}
            ],
            "completed": [
                {"task": "メール", "priority": "高", "timestamp": 1670390400.0}
            ]
        }
        # ToDoListオブジェクトを作成
        self.todo_list = ToDoList("test_todo.json")
        # タスクリストを初期化
        self.todo_list.tasks = {"active": [], "completed": []}

    def test_load_data(self):
        """
        load_dataメソッドのテスト
        """
        # モックデータをJSON形式に変換
        mock_data = json.dumps(self.test_data, ensure_ascii=False)
        # open関数をモックに置き換え
        with patch("builtins.open", mock_open(read_data=mock_data)):
            # load_dataメソッドを実行
            loaded_data = self.todo_list.load_data()
        # 読み込んだデータとテストデータが一致することを確認
        self.assertDictEqual(loaded_data, self.test_data)

    @patch("builtins.open", mock_open())
    def test_save_data(self):
        """
        save_dataメソッドのテスト
        """
        # タスクリストにテストデータを設定
        self.todo_list.tasks = self.test_data
        # save_dataメソッドを実行
        self.todo_list.save_data()

    def test_add_task(self):
        """
        add_taskメソッドのテスト
        """
        # タスクを追加
        self.todo_list.add_task("散歩", "低")
        # アクティブなタスクを取得
        tasks = self.todo_list.get_active_tasks()
        # タスク数が1つであることを確認
        self.assertEqual(len(tasks), 1)
        # 追加したタスクの内容を確認
        self.assertEqual(tasks[0]["task"], "散歩")
        self.assertEqual(tasks[0]["priority"], "低")

    def test_complete_task(self):
        """
        complete_taskメソッドのテスト
        """
        # タスクリストにテストデータをコピー
        self.todo_list.tasks = self.test_data.copy()
        # タスクを完了済みへ移動
        self.todo_list.complete_task(1)
        # アクティブなタスクと完了済みのタスクを取得
        active_tasks = self.todo_list.get_active_tasks()
        completed_tasks = self.todo_list.get_completed_tasks()
        # アクティブなタスクと完了済みのタスクの数が正しいことを確認
        self.assertEqual(len(active_tasks), 2)
        self.assertEqual(len(completed_tasks), 2)
        # 完了済みへ移動したタスクが正しいことを確認
        self.assertEqual(completed_tasks[-1]['task'], '掃除')

    def test_set_priority(self):
        """
        set_priorityメソッドのテスト
        """
        # タスクリストにテストデータをコピー
        self.todo_list.tasks = self.test_data.copy()
        # タスクの優先度を変更
        self.todo_list.set_priority(0, "低")
        # アクティブなタスクを取得
        tasks = self.todo_list.get_active_tasks()
        # 変更後の優先度が正しいことを確認
        self.assertEqual(tasks[0]["priority"], "低")

    def test_search_tasks(self):
        """
        search_tasksメソッドのテスト
        """
        # タスクリストにテストデータをコピー
        self.todo_list.tasks = self.test_data.copy()
        # キーワードでタスクを検索
        result = self.todo_list.search_tasks("買")
        # 検索結果が正しいことを確認
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["task"], "買い物")

    def test_sort_tasks_by_priority(self):
        """
        sort_tasksメソッドの優先度ソートのテスト
        """
        # タスクリストにテストデータをコピー
        self.todo_list.tasks = self.test_data.copy()
        # 優先度でソート
        self.todo_list.sort_tasks("priority")
        # アクティブなタスクを取得
        tasks = self.todo_list.get_active_tasks()
        # ソート結果が正しいことを確認
        self.assertEqual(tasks[0]["priority"], "高")
        self.assertEqual(tasks[1]["priority"], "中")
        self.assertEqual(tasks[2]["priority"], "低")

    def test_sort_tasks_by_timestamp(self):
        """
        sort_tasksメソッドのタイムスタンプソートのテスト
        """
        # タスクリストにテストデータをコピー
        self.todo_list.tasks = self.test_data.copy()
        # タイムスタンプでソート
        self.todo_list.sort_tasks("timestamp")
        # アクティブなタスクを取得
        tasks = self.todo_list.get_active_tasks()
        # ソート結果が正しいことを確認
        self.assertLess(tasks[0]["timestamp"], tasks[1]["timestamp"])
        self.assertLess(tasks[1]["timestamp"], tasks[2]["timestamp"])

# テストを実行
unittest.main()