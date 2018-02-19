import unittest


class TestReadOrders(unittest.TestCase):

    def test_read_orders(self):
        from cohort import read_orders
        from datetime import datetime
        import pytz
        from pytz import timezone

        expected_dict = {}
        expected_dict["10"] = [
            datetime.strptime('5/26/2014 21:10', '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC).astimezone(
                timezone('US/Pacific')),
            datetime.strptime('5/29/2014 20:18', '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC).astimezone(
                timezone('US/Pacific'))]

        order_dict = read_orders('two_orders.csv')

        self.assertEqual(order_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
