from unittest import TestCase


class TestRead_orders(TestCase):
    """
    def test_read_orders(self):
        from cohort import read_orders
        self.assertEqual(read_orders('orders.csv'), 5)
    """

    def test_read_orders2(self):
        from cohort import read_customers
        from datetime import datetime
        import pytz
        from pytz import timezone

        expected_date = '7/3/2015 22:01'
        expected_date = datetime.strptime(expected_date, '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC)
        expected_date = expected_date.astimezone(timezone('US/Pacific'))
        expected_date = expected_date.replace(hour=00, minute=00, second=00)
        expected_dict = {}
        expected_dict["35410"] = expected_date
        self.assertEqual(read_customers('customers_empty.csv'), expected_dict, expected_date)
