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
        for row in my_reader:  # Each row a list with one element
            line_counter = line_counter + 1
            if line_counter > 1:  # Because columns have headers
                line_list = (' '.join(row)).split(',')  # Each row to string and then to list with elements
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
        for row in my_reader:  # Each row a list with one element
            line_counter = line_counter + 1
            if line_counter > 1:  # Because columns have headers
                line_list = (' '.join(row)).split(',')  # Each row to string and then to list with elements
                # order_id = line_list[0]
                # order_number = line_list[1]
                cost_id = line_list[2]
                date = line_list[3]
                date_utc = datetime.strptime(date, '%m/%d/%Y %H:%M').replace(tzinfo=pytz.UTC)
                date_grouping_timezone = date_utc.astimezone(timezone(grouping_timezone))
                if cost_id in order_dict:  # If user has previously made an order
                    order_dict[cost_id].append(date_grouping_timezone)  # dictionary--> user_id : list_of_dates
                else:
                    temp_list = [date_grouping_timezone]
                    order_dict[cost_id] = temp_list


def cohort_analysis(starting_period, week_cohort_count, final_matrix):
    # print("min_period cohort_analysis")
    # print(starting_period)
    final_day_last_period = starting_period + timedelta(days=7 * cohorts)
    # print("end_period 1")
    # print(final_day_last_period)
    final_day_last_period = datetime.combine(final_day_last_period, datetime.min.time())
    # print("end_period 2")
    # print(final_day_last_period)
    final_day_last_period = final_day_last_period.astimezone(timezone(grouping_timezone))
    print("final_day_last_period")
    print(final_day_last_period)

    for c in costumer_dict.keys():
        create_account_day = costumer_dict[c]
        # print("create_account_day")
        # print(create_account_day)

        if create_account_day < final_day_last_period:  # If costumer is inside our cohorts

            # Add costumer at the corresponding cohort
            i = 1
            period = starting_period + timedelta(days=7 * i)
            period = datetime.combine(period, datetime.min.time())
            period = period.astimezone(timezone(grouping_timezone))
            while create_account_day >= period:
                i = i + 1
                period = starting_period + timedelta(days=7 * i)
                period = datetime.combine(period, datetime.min.time())
                period = period.astimezone(timezone(grouping_timezone))
            to_cohort = i - 1
            week_cohort_count[to_cohort] = week_cohort_count[to_cohort] + 1

            if c in order_dict:
                # print(c)
                order_dict[c].sort()
                j = 1
                gate = True
                # List with 0 or 1 for order into bucket - last one shows bucket for 1st order
                bucket_order = [-1 for k in range(buckets + 1)]

                for i in range(0, len(order_dict[c])):
                    while order_dict[c][i] > create_account_day + timedelta(days=j * 7) and j < buckets:
                        j = j + 1
                    if order_dict[c][i] < create_account_day + timedelta(days=j * 7):
                        bucket_order[j - 1] = 1
                        if gate:
                            bucket_order[buckets] = j - 1
                            gate = None

                for i in range(buckets):
                    if bucket_order[i] != -1:
                        final_matrix[to_cohort][i] = final_matrix[to_cohort][i] + 1
                if bucket_order[buckets] != -1:
                    final_matrix[to_cohort][bucket_order[buckets] + buckets] = final_matrix[to_cohort][
                                                                                   bucket_order[buckets] + buckets] + 1


def results_to_file(file_name):
    print("Result to {} file\n".format(file_name))
    with open(file_name, 'w', newline='') as csvfile:
        my_writer = csv.writer(csvfile)

        first_row = ['Cohort', 'Customers']
        bucket_from = 0
        for i in range(buckets):
            bucket_to = bucket_from + 6
            temp = "%s-%s days" % (bucket_from, bucket_to)
            # print(temp)
            first_row.append(temp)
            bucket_from = bucket_from + 7
        my_writer.writerow(first_row)

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
                    costumer_portion = (int(final_matrix[i][j]) * 100) / int(week_cohort_count[i])
                    first_time_portion = (int(final_matrix[i][buckets + j]) * 100) / int(week_cohort_count[i])
                    temp = "%.2f%% costumers (%s)\n%.2f%% 1st time (%s)" % (
                        costumer_portion, final_matrix[i][j], first_time_portion, final_matrix[i][buckets + j])
                else:
                    temp = ""
                other_row.append(temp)

            my_writer.writerow(other_row)
            other_row.clear()


if __name__ == '__main__':

    print("Hello. Let's start")

    for arg in sys.argv[1:]:
        print(arg)

    cohorts = 10
    # cohorts = int(sys.argv[1])
    buckets = 10
    # buckets = int(sys.argv[2])
    costumers_file_name = 'customers.csv'
    orders_file_name = 'orders.csv'
    result_file_name = 'CohortAnalysis2.csv'

    print("Performing Cohort Analysis with %d cohorts and %d buckets . . .\n" % (cohorts, buckets))

    starting_period = read_customers(costumers_file_name)
    print("min_period main")
    print(starting_period)

    read_orders(orders_file_name)

    # List to store the number of costumers in each cohort
    week_cohort_count = [0 for i in range(cohorts)]

    """2 dimensional list with final results
    for each line the first val(bucket) numbers are showing the number of orders to that bucket
    and the rest val(bucket) numbers are showing the first time orders to that bucket
    """
    final_matrix = [[0 for i in range(buckets * 2)] for j in range(cohorts)]

    cohort_analysis(starting_period, week_cohort_count, final_matrix)

    results_to_file(result_file_name)

    print("Goodbye!\n")
