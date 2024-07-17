## unittest_demo

このリポジトリは、Pythonのunittestモジュールを使ったユニットテストのデモです。

### プロジェクトの構成

* `simple_calculator.py`: Calculatorクラスと、そのクラスの各メソッドをテストするTestCalculatorクラスが含まれています。
* `simple_address.py`: ZipCodeSearcherクラスと、モックオブジェクトを使ったテストと実際のAPI呼び出しを使ったテストを含むTestZipCodeSearcherクラスが含まれています。
* `task.py`: ToDoListクラスとそのクラスの各メソッドをテストするTestToDoListAdvancedクラスが含まれています。このテストクラスでは、モックオブジェクトを使用したファイル操作のテストも含まれています。

### 各ファイルの説明

#### simple_calculator.py

基本的な四則演算（加算、減算、乗算、除算）を行うCalculatorクラスと、そのクラスの各メソッドをテストするTestCalculatorクラスが含まれています。
`TestCalculator`クラスでは、各演算が正しく行われるかを検証するテストケースが定義されています。

#### simple_address.py

郵便番号から住所を取得するZipCodeSearcherクラスと、そのクラスをテストするTestZipCodeSearcherクラスが含まれています。
`TestZipCodeSearcher`クラスには、モックオブジェクトを使ってAPI呼び出しを模倣するテストケースと、
実際のAPI呼び出しを行うテストケースの2つが定義されています。

#### task.py

ToDoリストを管理するToDoListクラスと、そのクラスをテストするTestToDoListAdvancedクラスが含まれています。
`ToDoList`クラスは、タスクの追加、完了、優先度設定、検索、ソートなどの機能を提供します。
`TestToDoListAdvanced`クラスでは、モックオブジェクトを使ってファイル入出力を模倣し、
各機能が正しく動作するかを検証するテストケースが定義されています。

### テストの実行方法

各Pythonファイルで、`unittest.main()` を実行することでテストを実行できます。
例えば、`simple_calculator.py` のテストを実行するには、以下のコマンドを実行します。

```bash
python simple_calculator.py
```


[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/deed.ja)
