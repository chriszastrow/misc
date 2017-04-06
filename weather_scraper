import re
import numpy
from urllib.request import urlopen
from lxml import html
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components


def run():
    '''Declare objects, establish source criteria, initiate data collection.'''
    data = {'cloud':[], 'real':[], 'feel':[], 'wind':[], 'rain':[], 'snow':[],
                        'ice':[], 'uv':[], 'cover':[], 'humid':[], 'dew':[]}
    source = {
        'base' : "_url_redacted_",
        'core' : "_url_redacted_",
        'mod' : numpy.arange(0, 73, 8),
        'step' : 1
    }
    data_collect(source, data)
    data_output(data)


def data_collect(source, data):
    '''Retreive the source data.'''
    while source['step'] < len(source['mod']):
        source_object = urlopen(source['base'] + source['core']
                                + str(source['mod'][source['step']])).read()
        soup = html.document_fromstring(source_object)
        source['step'] += 1
        data_process(data, soup)


def data_process(data, soup):
    '''Clean up & catalog the data.'''
    counter = 0
    #### Parse with cssselect of find_all with ('tag chain here'):
    for element in soup.cssselect('td span'):
        if counter < 8:
            data['cloud'].append(str(element.text))
        else:
            # Regex; strip superfluous characters & cast elements as int:
            element = int(re.sub("[^0-9^.]", "", str(element.text)))
            if counter < 16:
                data['real'].append(element)
            elif counter < 24:
                data['feel'].append(element)
            elif counter < 32:
                data['wind'].append(element)
            elif counter < 40:
                data['rain'].append(element)
            elif counter < 48:
                data['snow'].append(element)
            elif counter < 56:
                data['ice'].append(element)
            elif counter < 64:
                data['uv'].append(element)
            elif counter < 72:
                data['cover'].append(element)
            elif counter < 80:
                data['humid'].append(element)
            elif counter < 88:
                data['dew'].append(element)
            else:
                print('Unexpected overflow in tag cascade.')
                break
        counter += 1


def data_output(data):
    '''Bokeh chart code generation & export to file.'''
    pdframe = pd.DataFrame(data)
    xaxis = numpy.linspace(0, 72, len(pdframe))

    p = figure(plot_width=500, plot_height=300, sizing_mode='scale_width',
               background_fill_color='#fdfdfd', title='Key: Yellow=Temp, Blue=Wind, Black=Clouds')
    p.vbar(xaxis, width=1, bottom=0, top=pdframe['cover'], color='#222333')
    p.line(xaxis, (pdframe['wind'] * 4), line_color='#2244cc', line_width=3)
    p.quad((xaxis - 0.45), (xaxis + 0.45), (pdframe['real'] + 1), (pdframe['real'] - 1), line_color='#333333', color="#dde999")
    p.xgrid[0].ticker.desired_num_ticks = 24
    p.toolbar.logo = None
    p.toolbar_location = None

    script, div = components(p)
    file_output = open('/path/filename.html', 'r+')
    file_output.truncate()
    file_output.write(script)
    file_output.write(div)
    file_output.close()


if __name__ == '__main__':
    run()
