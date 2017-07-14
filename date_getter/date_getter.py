# config:utf-8

import datetime

saveDataFilePath = ""

last_day_not_leap = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
last_day_leap = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Get latest date from save.log file
def GetSavedDate():
    latest_date = 0
    try:
        f = open(saveDataFilePath, 'r')
        line = f.readline()
        while line:
            if line > latest_date:
                latest_date = line
            line = f.readline()
        f.close()
    except IOError:
        print "cannot open save data"
        return 0

    return latest_date

# split to year, month, date
# input data is number.
# Example input "20170707" output [2017, 7, 7s]
def SplitToYMD(date):
    date_year = int(date/10000)
    date_month = int((date - date_year*10000)/100)
    date_day = int((date - date_year*10000 - date_month*100))

    return [date_year, date_month, date_day]

def isLeapYear(year):
    if year%4 == 0:
        if year%100 == 0:
            if year%400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

def GetUpdateList():
    #savedDate = GetSavedDate()
    savedDate = 20150112
    print savedDate
    sDate = SplitToYMD(savedDate)

    begin_year = sDate[0]
    begin_month = sDate[1]
    begin_day = sDate[2]

    if isLeapYear(begin_year):
        last_day = last_day_leap
    else:
        last_day = last_day_not_leap

    if begin_day+1 > last_day[begin_month]:
        begin_month = begin_month + 1
        begin_day = 1
    else:
        begin_day = begin_day + 1

    today = datetime.date.today()
    todayDate = today.year*10000 + today.month*100 + today.day

    end_year = today.year
    end_month = today.month
    end_day = today.day

    update_list = []
    if savedDate+1 == todayDate:
        update_list.append(todayDate)
        return update_list

    if savedDate < todayDate:
        if begin_year == end_year:
            if isLeapYear(begin_year):
                last_day = last_day_leap
            else:
                last_day = last_day_not_leap

            if begin_month == end_month:
                for num in range(begin_day, end_day+1):
                    d = begin_year*10000 + begin_month*100 + num
                    print d
                    update_list.append(d)
            else:
                for num in range(begin_day, last_day[begin_month]+1):
                    update = begin_year*10000 + begin_month*100 + num
                    print update
                    update_list.append(update)
                for month in range(begin_month+1, end_month):
                    for day in range(1, last_day[month]+1):
                        update = begin_year*10000 + month*100 + day
                        print update
                        update_list.append(update)
                for num in range(1, end_day+1):
                    update = end_year*10000 + end_month*100 + num
                    print update
                    update_list.append(update)
        else:
            # first check begin_year
            if isLeapYear(begin_year):
                last_day = last_day_leap
            else:
                last_day = last_day_not_leap

            for num in range(begin_day, last_day[begin_month]+1):
                update = begin_year*10000 + begin_month*100 + num
                print update
                update_list.append(update)
            if begin_month < 12:
                for num in range(begin_month+1, 12+1):
                    for day in range(1, last_day[num]+1):
                        update = begin_year*10000 + num*100 + day
                        print update
                        update_list.append(update)

            # second check between begin_year and end_year
            if begin_year+1 < end_year:
                for year in range(begin_year+1, end_year):
                    if isLeapYear(year):
                        last_day = last_day_leap
                    else:
                        last_day = last_day_not_leap

                    for month in range(1, 13):
                        for day in range(1, last_day[month]+1):
                            update = year*10000 + month*100 + day
                            print update
                            update_list.append(update)

            # at last check end_year
            if isLeapYear(end_year):
                last_day = last_day_leap
            else:
                last_day = last_day_not_leap

            for month in range(1, end_month):
                for day in range(1, last_day[month]+1):
                    update = end_year*10000 + month*100 + day
                    print update
                    update_list.append(update)
            for day in range(1, last_day[end_month]+1):
                update = end_year*10000 + end_month*100 + day
                print update
                update_list.append(update)
    else:
        print "error"
    return update_list


def SaveLatestDate(latest_date):
    f = open(saveDataFilePath, "w")
    f.write(latest_date)
    f.close

if __name__ == '__main__':
    update_list = GetUpdateList()
