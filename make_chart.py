'''Make Bokeh chart html from JSON format stock history data files'''
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components

def write_chart_html_file(symbol):
    '''Create Pandas DataFrame from JSON format file'''
    file = open('/path/' + symbol + '.json', 'r+')
    df = pd.read_json(file)

    width_bar = 2*60*60*1000
    width_body = 12*60*60*1000 # widths as datetime values in ms.
    p = figure(x_axis_type='datetime', plot_width=500, plot_height=300, sizing_mode='scale_width',
            background_fill_color='#fdfdfd', title='Last Ten Trading Days')
    p.xaxis.major_label_orientation = 1
    p.grid.grid_line_alpha=0.3
    p.grid.grid_line_color='black'
    p.xgrid[0].ticker.desired_num_ticks = 10
    p.toolbar.logo = None
    p.toolbar_location = None
    p.vbar(df['date'], width_bar, df['high'], df['low'],
           fill_color="black", line_color="black")
    p.vbar(df['date'], width_body, df['open'], df['close'],
           fill_color=df['color_body'], line_color=df['color_body'])

    # export component div & script for html insertion:
    script, div = components(p)
    file_output = open('/path/' + symbol + '.html', 'r+')
    file_output.truncate()
    file_output.write(script)
    file_output.write(div)
    file_output.close()
    file.close()

def run():
    stockSymbols = ['MSFT', 'AAPL', 'GOOG']
    for symbol in stockSymbols:
        write_chart_html_file(symbol)

if __name__ == '__main__':
    run()
