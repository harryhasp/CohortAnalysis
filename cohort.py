import csv
import sys
from datetime import datetime
from datetime import timedelta


if __name__ == '__main__' :

    print("Hello. Let's start")

    for arg in sys.argv[1:] :
        print (arg)

    cohorts = 30
    #cohorts = int(sys.argv[1])
    buckets = 10
    #buckets = int(sys.argv[2])

    print("Performing Cohort Analysis with %d cohorts and %d buckets . . ." %(cohorts, buckets))

    #with open('C:\\Users\\sir7o\\PycharmProjects\\invitae\\customers.csv', newline='') as csvfile :
    with open('customers.csv', newline='') as csvfile:
        myReader = csv.reader(csvfile, delimiter='|')
        counter = 0
        #dateList = []
        costDict = {}
        for row in myReader: # each row a list with one element
            counter = counter + 1
            #if counter <= 10 and counter > 1 :
            if counter > 1:
                #print(row)
                lineList = (' '.join(row)).split(',') # each row to string and then to list with elements
                #print(lineList)
                id = lineList[0]
                #print("id: %s" %id)
                date = lineList[1]
                #print("date: %s" %date)
                newdate = datetime.strptime(date, '%m/%d/%Y %H:%M')
                #print(newdate)
                #dateList.append(newdate)
                costDict[id] = newdate # dictionary--> id : date
                #print()

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

    minKey = min(costDict, key=costDict.get)
    minPeriod = (costDict[minKey]).date()
    #print(minPeriod)

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


    #with open('C:\\Users\\sir7o\\PycharmProjects\\invitae\\orders.csv', newline='') as csvfile :
    with open('orders.csv', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter='|')
        counter = 0
        orderDict = {}
        for row in myreader: # each row a list with one element
            counter = counter + 1
            #if counter <= 1000 and counter > 1 :
            if counter > 1:
            #if counter > 1:
                #print(row)
                lineList = (' '.join(row)).split(',') # each row to string and then to list with elements
                #print(lineList)
                id = lineList[0]
                #print("id: %s" %id)
                order_number = lineList[1]
                #print("order_number: %s" % order_number)
                user_id = lineList[2]
                #print("user_id: %s" % user_id)
                date = lineList[3]
                #print("date: %s" %date)
                newdate = datetime.strptime(date, '%m/%d/%Y %H:%M')
                #print(newdate)
                #orderDict[user_id] = orderDict[user_id].append(newdate)
                if user_id in orderDict :
                    orderDict[user_id].append(newdate) # dictionary--> user_id : list_of_dates
                else :
                    tempList = [newdate]
                    orderDict[user_id] = tempList

    #print(orderDict)

    """
    print(orderDict['9568'])
    print(len(orderDict['9568']))
    createDay = costDict['9568']
    print(createDay)
    for pray in range(1,11) :
        print(createDay + timedelta(days=pray*7))
    """

    # list reusable for each costumer
    bucketOrder = []
    # for testing - to DEL
    testbucketOrder = []
    # list to store the number of costumers in each cohort
    weekCohortCount = [0 for i in range(cohorts)]
    # final result
    finalMatrix = [[0 for i in range(buckets*2)] for j in range(cohorts)]

    for c in costDict.keys() :
        createAccountDay = costDict[c]

        endPeriod = minPeriod + timedelta(days = 7*cohorts)
        endPeriod = datetime.combine(endPeriod, datetime.min.time())
        #print(period)

        # if costumer is inside our cohorts
        if createAccountDay < endPeriod :

            # add him at the corresponding cohort
            i = 1
            period = minPeriod + timedelta(days = 7*i)
            period = datetime.combine(period, datetime.min.time())
            while createAccountDay >= period :
                i = i + 1
                period = minPeriod + timedelta(days=7 * i)
                period = datetime.combine(period, datetime.min.time())
            toCohort = i - 1
            weekCohortCount[toCohort] = weekCohortCount[toCohort] + 1


            if c in orderDict :
                #print(c)
                orderDict[c].sort()
                j = 1
                gate = True
                #gate2 = None # to DEL
                # dictionary--> user_id : list with 0 or 1 for order into bucket - last one shows bucket for 1st order
                bucketOrder = [-1 for k in range(buckets + 1)]

                for i in range(0,len(orderDict[c])) :
                    gate2 = None
                    while orderDict[c][i] > createAccountDay + timedelta(days=j * 7) and j < buckets:
                        j = j + 1
                    if orderDict[c][i] < createAccountDay + timedelta(days=j * 7):
                        bucketOrder[j - 1] = 1
                        if gate:
                            bucketOrder[buckets] = j - 1
                            gate = None
                """           
                if c == '9568' : # for testing - to DEL
                    testbucketOrder = bucketOrder
                """

                for i in range(buckets) :
                    if bucketOrder[i] != -1 :
                        finalMatrix[toCohort][i] = finalMatrix[toCohort][i] + 1
                if bucketOrder[buckets] != -1 :
                    finalMatrix[toCohort][bucketOrder[buckets]+buckets] = finalMatrix[toCohort][bucketOrder[buckets]+buckets] + 1

    """
    for i in range(cohorts) :
        print(finalMatrix[i])
    """

    print("Result to CohortAnalysis.csv file")
    with open('CohortAnalysis.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)

        firstRow = ['Cohort', 'Customers']
        bucketFrom = 0
        for i in range(buckets) :
            bucketTo = bucketFrom + 6
            temp = "%s-%s days"%(bucketFrom,bucketTo)
            #print(temp)
            firstRow.append(temp)
            bucketFrom = bucketFrom + 7
        spamwriter.writerow(firstRow)

        dateFrom = minPeriod
        otherRow = []
        for i in range(cohorts) :
            dateFromStr = dateFrom.strftime("%m/%d/%y")
            dateTo = dateFrom + timedelta(days=6)
            dateToStr = dateTo.strftime("%m/%d/%y")
            temp = "%s - %s" % (dateFromStr, dateToStr)
            #print(temp)
            otherRow.append(temp)
            dateFrom = dateTo + timedelta(days=1)

            temp = "%s costumers" %(weekCohortCount[i])
            otherRow.append(temp)

            for j in range(buckets) :
                if int(finalMatrix[i][j]) > 0 :
                    portion1 = (int(finalMatrix[i][j]) * 100)/int(weekCohortCount[i])
                    portion2 = (int(finalMatrix[i][buckets+j]) * 100) / int(weekCohortCount[i])
                    temp = "%.2f%% costumers (%s)\n%.2f%% 1st time (%s)" % (portion1, finalMatrix[i][j], portion2, finalMatrix[i][buckets+j])
                else :
                    temp = ""
                otherRow.append(temp)

                #otherRow.append(finalMatrix[i])

            spamwriter.writerow(otherRow)
            otherRow.clear()

    """
    print()
    #print(orderDict)
    print(orderDict['9568'])
    print(testbucketOrder)
    print(weekCohortCount)
    print(len(orderDict.keys()))
    print(len(costDict.keys()))
    """

    print("Goodbye!")

























