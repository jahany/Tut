import unittest
from scripts.Services.weightsensor import WeightSensorWorker


class TestWeightSensor(unittest.TestCase):
    def setUp(self) -> None:
        self.sensor = WeightSensorWorker()
        
    def test_remove_outlier(self):
        data_list = [1, 2, 3, 4, 100]
        result = self.sensor.outlierRemover(data_list)
        self.assertEqual(result, 2)
        
    def test_no_outlier(self):
        data_list = [1, 2, 3, 4, 5]
        result = self.sensor.outlierRemover(data_list)
        self.assertEqual(result, 3)
        
    def test_run_noise_reduction_buffer(self):
        noise_reduction_buffer = [ 1, 2 , 3 , 4 , 100]
        read_weight_buffer = self.sensor.outlierRemover(noise_reduction_buffer)
        self.assertEqual(read_weight_buffer, 2)
        
    def test_get_current_weight(self):
        noise_reduction_buffer = [ 1, 2 , 3 , 4 , 100]
        read_weight_buffer = self.sensor.outlierRemover(noise_reduction_buffer)
        set_weight = self.sensor.setcurrentweight(read_weight_buffer)
        get_weight = self.sensor.getcurrentweight()
        self.assertEqual(get_weight, 2)
                
        
        
if __name__ == '__main__':
    unittest.main()