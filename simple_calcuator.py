import unittest

class Calculator:
    def add(self, x, y):
        """2つの数値を加算する"""
        return x + y

    def subtract(self, x, y):
        """2つの数値を減算する"""
        return x - y

    def multiply(self, x, y):
        """2つの数値を乗算する"""
        return x * y

    def divide(self, x, y):
        """2つの数値を除算する
        
        ゼロ除算を回避するため、yが0の場合はZeroDivisionErrorを発生させる
        """
        if y == 0:
            raise ZeroDivisionError("0で割ることはできません")
        return x / y

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """テストケース実行前に、Calculatorクラスのインスタンスを作成する"""
        self.calculator = Calculator()

    def test_add(self):
        """加算のテスト"""
        self.assertEqual(self.calculator.add(2, 3), 5)
        self.assertEqual(self.calculator.add(-2, 3), 1)
        self.assertEqual(self.calculator.add(2, -3), -1)

    def test_subtract(self):
        """減算のテスト"""
        self.assertEqual(self.calculator.subtract(5, 3), 2)
        self.assertEqual(self.calculator.subtract(3, 5), -2)
        self.assertEqual(self.calculator.subtract(-5, -3), -2)

    def test_multiply(self):
        """乗算のテスト"""
        self.assertEqual(self.calculator.multiply(2, 3), 6)
        self.assertEqual(self.calculator.multiply(-2, 3), -6)
        self.assertEqual(self.calculator.multiply(2, -3), -6)

    def test_divide(self):
        """除算のテスト"""
        self.assertEqual(self.calculator.divide(6, 3), 2)
        self.assertEqual(self.calculator.divide(6, -3), -2)
        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide(6, 0)

if __name__ == '__main__':
    unittest.main()