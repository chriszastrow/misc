'''Create fictional data set for call center inbound call handling capacity analysis'''
import pandas as pd
import numpy as np
import datetime

def generate_call_records():
    '''Initialize the dataframe prior to record creation & insertion'''
    index = range(0, 0)
    columns = ['Interval', 'TimeStamp', 'Group', 'WaitTime', 'ServiceTime', 'Result',
               'IntervalCall', 'IntervalAban', 'IntervalMeanWait', 'IntervalMeanService', 'Label']
    df = pd.DataFrame(index=index, columns=columns)
    return df

def cdn(df):
    '''Reduce max_calls by percentage per interval, send each call to be processed by Agent'''
    interval = 0
    max_calls = 200
    # Per-interval modifier (percentage of max_calls):
    percentage = [10, 20, 40, 60, 60, 50, 40, 40, 50, 60, 70, 90, 100, 100, 90, 80, 80, 70, 70, 60, 40, 30, 20, 10]
    for i in range(0,24):
        interval += 1
        volume = int((max_calls - np.random.randint(0,20))/100)*percentage[i] #rand increase, reduce by %
        for n in range(0,volume):
            agent(df,interval,volume)

def agent(df,interval,volume):
    '''Each call is received and defined by Agent function, result is single row entry to dataframe'''
    num = len(df)
    df.set_value(num, 'Interval', interval)
    timestamp = datetime.timedelta(seconds=(((interval/2)+8)*3600)+(np.random.randint(0,1800)))
    df.set_value(num, 'TimeStamp', str(timestamp))
    group = np.random.choice(['1st Line','2nd Line','800 Line','Backup','Help Line'], 1, p=[0.42, 0.33, 0.14, 0.06, 0.05])
    df.set_value(num, 'Group', group[0])#group[0] is the (weighted) random choice result element
    waittime = np.random.randint(int(volume/10),int(volume)*5)
    patience = np.random.randint(int(volume/5),int(volume)*15)
    if patience < waittime: #If caller waittime exceeds patience, abandon is True.
        df.set_value(num, 'Result', 'abandoned')
        df.set_value(num, 'WaitTime', patience)
        df.set_value(num, 'ServiceTime', 0)
    else:
        df.set_value(num, 'Result', 'serviced')
        df.set_value(num, 'WaitTime', waittime)
        servicetime = np.random.randint(0,900)
        df.set_value(num, 'ServiceTime', servicetime)

def process(df):
    '''Insert calls, abandons, means (exclude abandons) per interval for each group:'''
    groups = df.Group.unique()
    intervals = df.Interval.unique()
    for g in groups:
        dfx = df[df.Group == g]
        for i in intervals:
            dfy = dfx[dfx.Interval == i]
            call_count = len(dfy)
            dfz = dfy[dfy.Result == 'abandoned']
            aban_count = len(dfz)
            dfw = dfy[dfy.Result != 'abandoned']
            mean_waittime = int(dfw.WaitTime.sum()/len(dfw)) if len(dfw) else 0
            mean_servicetime = int(dfw.ServiceTime.sum()/len(dfw)) if len(dfw) else 0
            for x in dfy.index:
                df.set_value(x, 'IntervalCall', call_count)
                df.set_value(x, 'IntervalAban', aban_count)
                df.set_value(x, 'IntervalMeanWait', mean_waittime)
                df.set_value(x, 'IntervalMeanService', mean_servicetime)

def run():
    df = generate_call_records()
    cdn(df)
    process(df)
    return df

if __name__ == '__main__':
    run()
