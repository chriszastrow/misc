'''Retrieve records from MySQL database; write to file in JSON format for use by chart creation script.'''
import MySQLdb
import datetime

def records_to_file(dataSources,stockSymbols,cursor):
    for symbol in stockSymbols:
        #### TODO: Change from 14 day retrieval attempt to 10 day success test.
        #### TODO: Append JSON file with single day instead of 10 day full rewrite.
        dateCount = 14
        file = open('/path/' + symbol + '.json', 'r+')
        file.truncate()
        file.write('[')
        write_count = 0

        while dateCount > 0:
            query_result = {}
            date = (datetime.date.today() - datetime.timedelta(days = dateCount))

            cursor.execute("SELECT `High` FROM `StockHistory` WHERE `Date` = (%s) \
            AND (`Source` = 'yahoo') AND (`Symbol` = (%s))", (date, symbol))
            if cursor.rowcount == 1:
                query_result['High'] = cursor.fetchone()[0]

            cursor.execute("SELECT `Open` FROM `StockHistory` WHERE `Date` = (%s) \
            AND (`Source` = 'yahoo') AND (`Symbol` = (%s))", (date, symbol))
            if cursor.rowcount == 1:
                query_result['Open'] = cursor.fetchone()[0]

            cursor.execute("SELECT `Close` FROM `StockHistory` WHERE `Date` = (%s) \
            AND (`Source` = 'yahoo') AND (`Symbol` = (%s))", (date, symbol))
            if cursor.rowcount == 1:
                query_result['Close'] = cursor.fetchone()[0]

            cursor.execute("SELECT `Low` FROM `StockHistory` WHERE `Date` = (%s) \
            AND (`Source` = 'yahoo') AND (`Symbol` = (%s))", (date, symbol))
            if cursor.rowcount == 1:
                query_result['Low'] = cursor.fetchone()[0]
                #### Do not write comma before first key/value pair, or after last:
                if write_count > 0 and write_count < 11:
                    file.write(',')
                write_count += 1
                #### Write to file, if cursor row count == 1:
                file.write('{"date":"' + str(date) + '",')
                file.write('"open":' + str(query_result["Open"]) + ',')
                file.write('"low":' + str(query_result["Low"]) + ',')
                file.write('"high":' + str(query_result["High"]) + ',')
                file.write('"close":' + str(query_result["Close"]) + ',')
                #### Set color (green/red) according to day gain or loss:
                body_color = "#66ad53" if query_result["Close"] >= query_result["Open"] else "#ad6653"
                file.write('"color_body":"' + body_color + '"}')

            dateCount -= 1

        file.write(']')
        file.close()

def run():
    #### Declare Variables:
    dataSources = ['yahoo', 'google']
    stockSymbols = ['MSFT', 'AAPL', 'GOOG']

    #### Connect to DB, retrieve records & write to file as JSON:
    connection = MySQLdb.connect("_url_", "_user_", "_pass_", "_database_")
    cursor = connection.cursor()
    records_to_file(dataSources,stockSymbols,cursor)
    cursor.close()
    connection.close()

if __name__ == '__main__':
    run()
