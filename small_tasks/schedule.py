import datetime as dt

# generate schedule from start_date
def generate_schedule(days: int, work_days: int, rest_days: int, start_date: dt.datetime):
       
    # check integer parameters' types
    if not all(isinstance(item, int) for item in (days, work_days, rest_days)):
        raise TypeError('Days, work_days and rest_days must be integer numbers')

    # check integer parameters' values
    if not all(item >= 0 for item in (days, work_days, rest_days)):
        raise ValueError('Days, work_days and rest_days can not be negative numbers')
    
    # check start_date
    if not isinstance(start_date, dt.datetime):
        raise TypeError('Start_date must have datetime type')
    
    # empty schedule
    if work_days == 0:
        return []
    
    # result list
    schedule = []
    # initial values
    i = 0
    work_i = 0

    # form schedule 
    while True:
        # increase index
        i += 1
        # skip rest days
        if work_i >= work_days and work_i % work_days == 0:
            i += rest_days        
        # check bound 
        if i > days:
            break
        # save next work day
        day = start_date + dt.timedelta(days=i-1)
        schedule.append(day)
        work_i += 1
    
    return schedule
 
# test
print(generate_schedule(5, 2, 1, dt.datetime(2020, 1, 30)))