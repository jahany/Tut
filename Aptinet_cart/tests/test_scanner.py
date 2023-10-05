import unittest
from unittest.mock import MagicMock
from scripts.Services.scanner import ScannerWorker


class TestScanner(unittest.TestCase):
    def setUp(self) -> None:
        self.scanner = ScannerWorker()
    
    def test_outOfLogic(self):
        self.assertFalse(self.scanner.out_of_logic)
        self.scanner.outOfLogic()
        self.assertTrue(self.scanner.out_of_logic)
        
    def test_baudrate_is_9600(self):
        self.assertEqual(self.scanner.ser.baudrate, 9600)
        

        
if __name__ == '__main__':
    unittest.main()