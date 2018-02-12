import csv
import sys
from datetime import datetime
from datetime import timedelta
import pytz
from pytz import timezone


if __name__ == '__main__':

    print("Hello. Let's start")

    for arg in sys.argv[1:]:
        print(arg)

    cohorts = 30
    # cohorts = int(sys.argv[1])
    buckets = 10
    # buckets = int(sys.argv[2])

    print("Performing Cohort Analysis with %d cohorts and %d buckets . . ." % (cohorts, buckets))

    # with open('C:\\Users\\sir7o\\PycharmProjects\\invitae\\customers.csv', newline='') as csvfile :
    with open('customers.csv', newline='') as csvfile:
        myReader = csv.reader(csvfile, delimiter='|')
        counter = 0
        tzinfo = pytz.UTC
        # dateList = []
        costumer_dict = {}
        for row in myReader:  # each row a list with one element
            counter = counter + 1
            # if counter <= 10 and counter > 1 :
            if counter > 1:
                # print(row)
                line_list = (' '.join(row)).split(',')  # each row to string and then to list with elements
                # print(lineList)
                id = line_list[0]
                # print("id: %s" %id)
                date = line_list[1]
                # print("date: %s" %date)
                new_date = datetime.strptime(date, '%m/%d/%Y %H:%M')
                # print(new_date)
                # dateList.append(new_date)
                costumer_dict[id] = new_date  # dictionary--> id : date
                # print()


                if counter == 2:
                    #tzinfo = pytz.UTC
                    print()
                    print(date)
                    print(new_date)
                    #tz = pytz.timezone('US/Pacific')
                    #print(tz)
                    #tz.zone
                    #print(tz.zone)
                    #localDatetime = new_date.astimezone(tzinfo)
                    #print(localDatetime)

                    #utc = pytz.utc
                    #print(utc)
                    #print(utc.zone)
                    #utc_dt = utc.localize(datetime.utcfromtimestamp(1143408899))
                    #print(utc_dt)
                    #now = datetime.datetime.utcnow()
                    #print(now)
                    print()


    """
    dateList.sort()
    #print(dateList)
    #print(dateList[0])
    print(min(dateList))
    minDate = dateList[0]
    print(dateList[0].date())
    minPeriod = dateList[0].date()
    print(minPeriod)
    """

    min_key = min(costumer_dict, key=costumer_dict.get)
    min_period = (costumer_dict[min_key]).date()
    # print(min_period)

    """
    period = dateList[0].date() + timedelta(days=7)
    period = datetime.combine(period, datetime.min.time())
    print(period)
    i = 0
    weekCohortCount = [0,0,0,0,0,0,0,0,0,0]
    for tempDate in dateList :
        if tempDate < period :
            weekCohortCount[i] = weekCohortCount[i] + 1
        else :
            i = i + 1
            if i == 10 :
                break
            weekCohortCount[i] = weekCohortCount[i] + 1
            period = period + timedelta(days=7)
            print(period)


    print(weekCohortCount)
    print()
    """

    # with open('C:\\Users\\sir7o\\PycharmProjects\\invitae\\orders.csv', newline='') as csvfile :
    with open('orders.csv', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter='|')
        counter = 0
        order_dict = {}
        for row in myreader:  # each row a list with one element
            counter = counter + 1
            # if counter <= 1000 and counter > 1 :
            if counter > 1:
                # if counter > 1:
                # print(row)
                line_list = (' '.join(row)).split(',')  # each row to string and then to list with elements
                # print(line_list)
                id = line_list[0]
                # print("id: %s" %id)
                order_number = line_list[1]
                # print("order_number: %s" % order_number)
                user_id = line_list[2]
                # print("user_id: %s" % user_id)
                date = line_list[3]
                # print("date: %s" %date)
                new_date = datetime.strptime(date, '%m/%d/%Y %H:%M')
                # print(new_date)
                # order_dict[user_id] = order_dict[user_id].append(new_date)
                if user_id in order_dict:
                    order_dict[user_id].append(new_date)  # dictionary--> user_id : list_of_dates
                else:
                    tempList = [new_date]
                    order_dict[user_id] = tempList

    # print(order_dict)

    """
    print(order_dict['9568'])
    print(len(order_dict['9568']))
    createDay = costumer_dict['9568']
    print(createDay)
    for pray in range(1,11) :
        print(createDay + timedelta(days=pray*7))
    """

    # list reusable for each costumer
    bucket_order = []
    # for testing - to DEL
    test_bucket_order = []
    # list to store the number of costumers in each cohort
    week_cohort_count = [0 for i in range(cohorts)]
    # final result
    final_matrix = [[0 for i in range(buckets * 2)] for j in range(cohorts)]

    for c in costumer_dict.keys():
        create_account_day = costumer_dict[c]

        end_period = min_period + timedelta(days=7 * cohorts)
        end_period = datetime.combine(end_period, datetime.min.time())
        # print(period)

        # if costumer is inside our cohorts
        if create_account_day < end_period:

            # add him at the corresponding cohort
            i = 1
            period = min_period + timedelta(days=7 * i)
            period = datetime.combine(period, datetime.min.time())
            while create_account_day >= period:
                i = i + 1
                period = min_period + timedelta(days=7 * i)
                period = datetime.combine(period, datetime.min.time())
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
    with open('CohortAnalysis.csv', 'w', newline='') as csvfile:
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

        date_from = min_period
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
