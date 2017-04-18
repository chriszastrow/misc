'''Collect stock performance data each day (via yahoo & google API); insert records into MySQL database.'''
import MySQLdb
import datetime
import pandas_datareader

def get_pdata(aStockSymbol,aDataSource,delta_days):
    '''Fetch data for specified Symbol, Source, First Delta Date, Last Delta Date:'''
    return pandas_datareader.DataReader(aStockSymbol, aDataSource,
        datetime.date.today() - datetime.timedelta(days = delta_days),
        datetime.date.today() - datetime.timedelta(days = delta_days))

def sql_insert_records(dataSources,stockSymbols,cursor,delta_days):
    '''Iterate each Source for each Symbol, collect data points & insert records to DB:'''
    while delta_days > 0:
        for valA in dataSources:
            for valB in stockSymbols:
                try:
                    pdata = get_pdata(valB,valA,delta_days)
                    cursor.execute("INSERT INTO `StockHistory` (\
                    `Source`, `Date`, `Symbol`, `Open`, `Close`, `High`, `Low`, `Volume`) VALUES (\
                    %s,%s,%s,TRUNCATE(%s,2),TRUNCATE(%s,2),TRUNCATE(%s,2),TRUNCATE(%s,2),%s)", (
                    valA, (str(pdata.index.values)[2:12]), valB, pdata.Open[0],
                    pdata.Close[0], pdata.High[0], pdata.Low[0], pdata.Volume[0]))
                except:
                    continue

        delta_days -= 1

def run():
    #### Declare Variables:
    dataSources = ['yahoo', 'google']
    stockSymbols = ['MSFT', 'AAPL', 'GOOG']
    #### How many days to go back to begin record collection?
    delta_days = 1

    #### Connect to DB, insert & commit records:
    connection = MySQLdb.connect("_url_", "_user_", "_pass_", "_database_")
    cursor = connection.cursor()
    sql_insert_records(dataSources,stockSymbols,cursor,delta_days)

    #### Commit SQL records & close connections:
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    run()
