import unittest


class TestReadCustomers(unittest.TestCase):

    def test_read_customers(self):
        from cohort import read_customers
        from datetime import datetime
        import pytz
        from pytz import timezone

        expected_date = datetime.strptime('5/26/2014 21:10', '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC).astimezone(
            timezone('US/Pacific'))
        expected_period = expected_date.replace(hour=00, minute=00, second=00)
        expected_dict = {}
        expected_dict["10"] = expected_date
        expected_dict["87"] = datetime.strptime('6/30/2014 3:21', '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC).astimezone(
            timezone('US/Pacific'))

        costumer_dict, starting_period = read_customers('two_customers.csv')

        self.assertEqual(expected_period, starting_period)

        self.assertEqual(expected_dict, costumer_dict)


if __name__ == '__main__':
    unittest.main()
