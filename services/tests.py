from django.test import TestCase
import datetime
from services.free_time import convert_period_to_set, test_calc_free_windows, calc_free_windows


class Test(TestCase):
    def test_convert_period_to_set(self):
        time_start = datetime.datetime(2022, 5, 1, 10, 0)
        time_end = datetime.datetime(2022, 5, 1, 11, 0)
        expected_result = {
            datetime.datetime(2022, 5, 1, 10, 0),
            datetime.datetime(2022, 5, 1, 10, 15),
            datetime.datetime(2022, 5, 1, 10, 30),
            datetime.datetime(2022, 5, 1, 10, 45),
            datetime.datetime(2022, 5, 1, 11, 0)
        }
        result = convert_period_to_set(time_start, time_end)
        self.assertSetEqual(result, expected_result)

    def test_string_convert_period_to_set(self):
        time_start = 'text'
        time_end = datetime.datetime(2022, 5, 1, 11, 0)
        with self.assertRaises(TypeError):
            convert_period_to_set(time_start, time_end)

    def test_reverse_convert_period_to_set(self):
        time_end = datetime.datetime(2022, 5, 1, 10, 0)
        time_start = datetime.datetime(2022, 5, 1, 11, 0)
        expected_result = set()
        result = convert_period_to_set(time_start, time_end)
        self.assertSetEqual(result, expected_result)

    def test_reverse_convert_period_to_set(self):
        time_start = datetime.datetime(2022, 5, 1, 10, 0)
        time_end = datetime.datetime(2022, 5, 1, 10, 0)
        expected_result = {datetime.datetime(2022, 5, 1, 10, 0)}
        result = convert_period_to_set(time_start, time_end)
        self.assertSetEqual(result, expected_result)

    def test_convert_period_to_set_with_timedelta(self):
        booking = [
            {
            'date': datetime.datetime(2022, 5, 1, 10, 0),
            'service_duration': 30
            }
        ]
        service_duration = 30
        work_time_start = datetime.datetime(2022, 5, 1, 10, 0)
        work_time_end = datetime.datetime(2022, 5, 1, 11, 0)
        result = test_calc_free_windows(booking, service_duration, work_time_start, work_time_end)
        expected_result = [datetime.datetime(2022, 5, 1, 10, 30)]
        self.assertListEqual(result, expected_result)
        ####################################

    def test_convert_period_to_set_with_timedelta_v2(self):
        booking = [
            {
                'date': datetime.datetime(2022, 5, 1, 10, 0),
                'service_duration': 30
            }
        ]
        service_duration = 30
        work_time_start = datetime.datetime(2022, 5, 1, 10, 0)
        work_time_end = datetime.datetime(2022, 5, 1, 12, 0)
        result = test_calc_free_windows(booking, service_duration, work_time_start, work_time_end)
        expected_result = [
                datetime.datetime(2022, 5, 1, 10, 30),
                datetime.datetime(2022, 5, 1, 10, 45),
                datetime.datetime(2022, 5, 1, 11, 00),
                datetime.datetime(2022, 5, 1, 11, 15),
                datetime.datetime(2022, 5, 1, 11, 30)
        ]
        self.assertListEqual(result, expected_result)
        #############################
    def test_convert_period_to_set_with_timedelta_v3(self):
        booking = [
            {
                'date': datetime.datetime(2022, 5, 1, 10, 0),
                'service_duration': 30
            },
            {
                'date': datetime.datetime(2022, 5, 1, 10, 30),
                'service_duration': 30
            }
        ]
        service_duration = 30
        work_time_start = datetime.datetime(2022, 5, 1, 10, 0)
        work_time_end = datetime.datetime(2022, 5, 1, 11, 0)
        result = test_calc_free_windows(booking, service_duration, work_time_start, work_time_end)

        expected_result = []
        self.assertListEqual(result, expected_result)
        #############################
    def test_convert_period_to_set_with_timedelta_v4(self):
        booking = [
            {
                'date': datetime.datetime(2022, 5, 1, 10, 0),
                'service_duration': 30
            },
            {
                'date': datetime.datetime(2022, 5, 1, 10, 30),
                'service_duration': 30
            }
        ]
        service_duration = 30
        work_time_start = datetime.datetime(2022, 5, 1, 10, 0)
        work_time_end = datetime.datetime(2022, 5, 1, 11, 30)
        result = test_calc_free_windows(booking, service_duration, work_time_start, work_time_end)

        expected_result = [datetime.datetime(2022, 5, 1, 11, 0)]
        self.assertListEqual(result, expected_result)

        #############################
    def test_convert_period_to_set_with_timedelta_v5(self):
        booking = [
            {
                'date': datetime.datetime(2022, 5, 1, 10, 0),
                'service_duration': 30
            },
            {
                'date': datetime.datetime(2022, 5, 1, 10, 45),
                'service_duration': 30
            }
        ]
        service_duration = 30
        work_time_start = datetime.datetime(2022, 5, 1, 10, 0)
        work_time_end = datetime.datetime(2022, 5, 1, 11, 30)
        result = test_calc_free_windows(booking, service_duration, work_time_start, work_time_end)

        expected_result = []
        self.assertListEqual(result, expected_result)
