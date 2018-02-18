import csv
import sys
from datetime import datetime
from datetime import timedelta
import pytz
from pytz import timezone

grouping_timezone = 'US/Pacific'
costumer_dict = {}
order_dict = {}


def read_customers(file_name):
    with open(file_name, newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter='|')
        line_counter = 0
        for row in my_reader:  # each row a list with one element
            line_counter = line_counter + 1
            if line_counter > 1:  # because columns have headers
                line_list = (' '.join(row)).split(',')  # each row to string and then to list with elements
                cost_id = line_list[0]
                date = line_list[1]
                date_utc = datetime.strptime(date, '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC)
                date_grouping_timezone = date_utc.astimezone(timezone(grouping_timezone))
                costumer_dict[cost_id] = date_grouping_timezone  # dictionary--> cost_id : date

    min_key = min(costumer_dict, key=costumer_dict.get)
    # print("costumer_dict[min_key]")
    # print(costumer_dict[min_key])
    starting_period = (costumer_dict[min_key]).replace(hour=00, minute=00, second=00)
    # min_period = (costumer_dict[min_key])
    print("min_period")
    print(starting_period)
    return starting_period


def read_orders(file_name):
    with open(file_name, newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter='|')
        line_counter = 0
        for row in my_reader:  # each row a list with one element
            line_counter = line_counter + 1
            if line_counter > 1:  # because columns have headers
                line_list = (' '.join(row)).split(',')  # each row to string and then to list with elements
                # order_id = line_list[0]
                # order_number = line_list[1]
                cost_id = line_list[2]
                date = line_list[3]
                date_utc = datetime.strptime(date, '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC)
                date_grouping_timezone = date_utc.astimezone(timezone(grouping_timezone))
                if cost_id in order_dict:  # if user has previously made an order
                    order_dict[cost_id].append(date_grouping_timezone)  # dictionary--> user_id : list_of_dates
                else:
                    temp_list = [date_grouping_timezone]
                    order_dict[cost_id] = temp_list


if __name__ == '__main__':

    print("Hello. Let's start")

    for arg in sys.argv[1:]:
        print(arg)

    cohorts = 10
    # cohorts = int(sys.argv[1])
    buckets = 10
    # buckets = int(sys.argv[2])

    print("Performing Cohort Analysis with %d cohorts and %d buckets . . ." % (cohorts, buckets))

    starting_period = read_customers('customers.csv', )
    print("min_period main")
    print(starting_period)

    read_orders('orders.csv', )

    # list reusable for each costumer
    bucket_order = []
    # for testing - to DEL
    test_bucket_order = []
    # list to store the number of costumers in each cohort
    week_cohort_count = [0 for i in range(cohorts)]
    # final result
    final_matrix = [[0 for i in range(buckets * 2)] for j in range(cohorts)]

    print("min_period")
    print(starting_period)
    end_period = starting_period + timedelta(days=7 * cohorts)
    print("end_period 1")
    print(end_period)
    end_period = datetime.combine(end_period, datetime.min.time())
    print("end_period 2")
    print(end_period)
    # end_period23 = datetime.strptime(end_period, '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC)
    end_period23 = end_period.astimezone(timezone('US/Pacific'))
    print("end_period 23")
    print(end_period23)

    for c in costumer_dict.keys():
        create_account_day = costumer_dict[c]
        # print("create_account_day")
        # print(create_account_day)
        # if costumer is inside our cohorts
        if create_account_day < end_period23:

            # add him at the corresponding cohort
            i = 1
            period = starting_period + timedelta(days=7 * i)
            period = datetime.combine(period, datetime.min.time())
            period = period.astimezone(timezone('US/Pacific'))
            while create_account_day >= period:
                i = i + 1
                period = starting_period + timedelta(days=7 * i)
                period = datetime.combine(period, datetime.min.time())
                period = period.astimezone(timezone('US/Pacific'))
            to_cohort = i - 1
            week_cohort_count[to_cohort] = week_cohort_count[to_cohort] + 1

            if c in order_dict:
                # print(c)
                order_dict[c].sort()
                j = 1
                gate = True
                # gate2 = None # to DEL
                # dictionary--> user_id : list with 0 or 1 for order into bucket - last one shows bucket for 1st order
                bucket_order = [-1 for k in range(buckets + 1)]

                for i in range(0, len(order_dict[c])):
                    gate2 = None
                    while order_dict[c][i] > create_account_day + timedelta(days=j * 7) and j < buckets:
                        j = j + 1
                    if order_dict[c][i] < create_account_day + timedelta(days=j * 7):
                        bucket_order[j - 1] = 1
                        if gate:
                            bucket_order[buckets] = j - 1
                            gate = None
                """           
                if c == '9568' : # for testing - to DEL
                    test_bucket_order = bucket_order
                """

                for i in range(buckets):
                    if bucket_order[i] != -1:
                        final_matrix[to_cohort][i] = final_matrix[to_cohort][i] + 1
                if bucket_order[buckets] != -1:
                    final_matrix[to_cohort][bucket_order[buckets] + buckets] = final_matrix[to_cohort][
                                                                                   bucket_order[buckets] + buckets] + 1

    """
    for i in range(cohorts) :
        print(final_matrix[i])
    """

    print("Result to CohortAnalysis.csv file")
    # with open('CohortAnalysis.csv', 'w', newline='') as csvfile:
    with open('CohortAnalysis2.csv', 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile)

        first_row = ['Cohort', 'Customers']
        bucket_from = 0
        for i in range(buckets):
            bucket_to = bucket_from + 6
            temp = "%s-%s days" % (bucket_from, bucket_to)
            # print(temp)
            first_row.append(temp)
            bucket_from = bucket_from + 7
        mywriter.writerow(first_row)

        date_from = starting_period
        other_row = []
        for i in range(cohorts):
            date_from_str = date_from.strftime("%m/%d/%y")
            date_to = date_from + timedelta(days=6)
            date_to_str = date_to.strftime("%m/%d/%y")
            temp = "%s - %s" % (date_from_str, date_to_str)
            # print(temp)
            other_row.append(temp)
            date_from = date_to + timedelta(days=1)

            temp = "%s costumers" % (week_cohort_count[i])
            other_row.append(temp)

            for j in range(buckets):
                if int(final_matrix[i][j]) > 0:
                    portion1 = (int(final_matrix[i][j]) * 100) / int(week_cohort_count[i])
                    portion2 = (int(final_matrix[i][buckets + j]) * 100) / int(week_cohort_count[i])
                    temp = "%.2f%% costumers (%s)\n%.2f%% 1st time (%s)" % (
                        portion1, final_matrix[i][j], portion2, final_matrix[i][buckets + j])
                else:
                    temp = ""
                other_row.append(temp)

                # other_row.append(final_matrix[i])

            mywriter.writerow(other_row)
            other_row.clear()

    """
    print()
    #print(order_dict)
    print(order_dict['9568'])
    print(test_bucket_order)
    print(week_cohort_count)
    print(len(order_dict.keys()))
    print(len(costumer_dict.keys()))
    """

    print("Goodbye!")
