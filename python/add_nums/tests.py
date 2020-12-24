import unittest

class TestStringMethods(unittest.TestCase):
    with open("cases.txt") as file:
        data = file.read()
        print(data)

if __name__ == '__main__':
    unittest.main()