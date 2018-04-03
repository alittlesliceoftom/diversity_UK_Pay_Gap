import seaborn as sb
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def import_data():
    df = pd.read_csv('UK Gender Pay Gap Data - 2017 to 2018.csv')
    return df

def explore():
    df.describe()

    df[df['DiffMeanHourlyPercent'] == -267.600000] ## wow these barlows peeps are a bit interesting

    barlow = df[df['DiffMeanHourlyPercent'] == -267.600000]


def create_synthetic_population_to_fit_stats():
    '''
    take a rows statistics, and work out what pay would have to be for various groups to give the aggregated level stats.
    :return:
    '''
    ##initially assume everyone in each category is paid the same.


    return

def getCompanyData(df,comp = 'Ovo'):
    '''Returns series of true falses. '''
    return df['EmployerName'].str.lower().str.contains(comp.lower())

###drawing section - to library
def drawVerticals(ax,df):
    #parity line
    ax.axvline(x=0,color = 'red')
    #median of medians
    # g.ax.axvline(x=df['DiffMedianHourlyPercent'].median(), label = 'median')
    #mean of means
    ax.axvline(x=df['DiffMeanHourlyPercent'].mean(),color = 'red', label = 'mean')
    return

def find_404s(url):
    '''check all the urls to find who's not even put a proper webpage in place'''
    import urllib.request
    status = 'URL Valid'
    if type(url) == float:
        if np.isnan(url):
            status = 'No URL Supplied'
        else:
            status = 'URL is number?'
    else:
        import re
        end = url[-6:]
        if re.search('com',end) or re.search('co.uk',end):
            status = 'URL is homepage'
        else:
            pass
        try:
            req = urllib.request.Request(url)
            try:
                urllib.request.urlopen(req)
                # print('Success')
            except urllib.error.URLError as e:
                # print(e.reason)
                status = e.reason
        except:
            print('url {} ill formed'.format(url))
            status = 'URL ill formed'
    return status

def sbPlot(df):
    ### explore median vs median
    sb.lmplot(x = 'DiffMeanHourlyPercent', y = 'DiffMedianHourlyPercent', hue = 'EmployerSize', data = df)
    #a bit different , but confusing, lets look at ratio with respect to mean

    df['mean/median'] = df['DiffMeanHourlyPercent'] / df['DiffMedianHourlyPercent']
    sb.lmplot(x = 'DiffMeanHourlyPercent', y = 'mean/median', hue = 'EmployerSize', data = df)

    ##wow some weird ones at the top there. Let's sort by the difference
    srt = df.sort_values(by = 'mean/median',axis = 'index', ascending = False)
    srt[srt['mean/median']<100000].head(4)
    ##looks like some of those big values are football clubs - which makes sense.

#quartiles on this graph are - top right, average and median man is paid more,
#bottom right, average man paid more, median woman paid more. Probably professional women, men at the top.
#Bottom left, women paid more average and median
#Top Left, women paid more on average, but less on median.

def bokeh_scatter(df, colourDimension = 'EmployerSize', title = "Mean (x)  vs Median (y) Scatter"):
    '''
    Make a scatter plot from a dataframe
    :param df:
    :param colors:
    :return:
    '''
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, HoverTool, TapTool , OpenURL
    from bokeh.transform import factor_cmap
    #bokeh data
    srce = ColumnDataSource(df[['DiffMeanHourlyPercent','DiffMedianHourlyPercent','CurrentName','EmployerSize','DiffMeanHourlyPercent','DiffMedianHourlyPercent','CompanyLinkToGPGInfo','Sector']])

    # output to static HTML file
    output_file("dots.html")

    # create a new plot
    p = figure(
       tools="pan,box_zoom,reset,save, tap", title=title,
       x_axis_label='mean gap %', y_axis_label='median gap %'
    )
    p.circle(source=srce, x='DiffMeanHourlyPercent', y='DiffMedianHourlyPercent', legend="y=x", color=colourDimension,
             fill_color=colourDimension, size=8)
    ##attempts to get colour grouping workings
    # color_map = CategoricalColorMapper(factors=df[colourDimension].unique())
    # p.circle(source=srce, x='DiffMeanHourlyPercent', y='DiffMedianHourlyPercent', legend="y=x", color={'field': colourDimension, 'transform': color_map}, size=8)


    url = '@CompanyLinkToGPGInfo/'
    #make the axes stand out -- got rid of this as couldn't work out how to
    # p.xaxis.axis_line_width = 3
    # p.yaxis.axis_line_width = 3
    # p.xaxis.axis_line_color = "Black"
    # p.xaxis.axis_line_join()
    # add some renderers
    # index_cmap = factor_cmap('DiffMeanHourlyPercent', palette = Spectral6,  factors=sorted(df[colourDimension].unique()), end=1)
    p.add_tools(HoverTool(tooltips=[("Name", "@CurrentName"), ("EmployerSize", "@EmployerSize"), ("MedianDiff", "@DiffMedianHourlyPercent"), ("MeanDiff", "@DiffMeanHourlyPercent")]))
    # p.add_tools(TapTool())
    # p.add_tools(TapTool(behaviour = '', tooltips=[("Name", "@CurrentName"), ("EmployerSize", "@EmployerSize"), ("MedianDiff", "@DiffMedianHourlyPercent"), ("MeanDiff", "@DiffMeanHourlyPercent")]))
    t = p.select(type = TapTool)
    t.callback = OpenURL(url = url )
    return p, t

from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, TapTool , OpenURL


def maybe_pickle(df):
    import pickle as p
    p.dump(df,'df.p')

def maybe_unpickle():
    import pickle as p
    p.load()

def classify_companies(df):
    '''
    This function will need work @todo.
    But adds a classification of what companies do - currently manual
    :return:
    '''
    df['Sector'] = None
    df.loc[getCompanyData(df, comp = 'Football Club'),'Sector']= 'Football'
    df.loc[getCompanyData(df, comp = 'Energy'),'Sector'] = 'Energy'
    df.loc[getCompanyData(df, comp = 'Tech'),'Sector'] = 'Tech'
    #edit objects pointing to wider df.
    # fc.loc['Sector'] = 'Football'
    # ec.loc['Sector'] = 'Energy'

if __name__ =='__main__':
    df = import_data()
    classify_companies(df)
    tc = df[df['Sector']=='Tech']
    p, t = bokeh_scatter(tc, title = 'Tech Company Pay Gaps   ', colourDimension = 'Sector')
    show(p)
    print(df.groupby(by = 'Sector').mean())

    ## test if the website link that company has provided actually works.
    urls = df['CompanyLinkToGPGInfo']
    #
    # df['URLWorks?'] = None
    # for i, r in df.iterrows():
    #     df['URLWorks?'][i] = find_404s(r['CompanyLinkToGPGInfo'])#
    #     if i%100 == 0:
    #         print (i) ##so can see how long it is taking.

    # maybe_pickle(df)