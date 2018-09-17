import geocoder
import requests
from bs4 import BeautifulSoup
import os
from functools import lru_cache
from bokeh.io import output_file,show
from bokeh.models import GMapPlot,GMapOptions,ColumnDataSource,Circle,Range1d,PanTool,WheelZoomTool,BoxSelectTool
lats=[]
lans=[]
def get_data():
    url="https://www.google.com/about/datacenters/inside/locations/index.html"
    data=requests.get(url)
    soup=BeautifulSoup(data.text,'html.parser')
    href=soup.find_all('a')
    for h in href:
        fopen=open('data.txt',mode='a+')
        data=str(h.text)
        try:
            s= data.split('\n   ')
            data=s[0].strip()+s[1].strip()
        except:
            pass
        if data is not '' and ',' in data:
            fopen.write(data+'\n')
    fopen.close()
@lru_cache(maxsize=1024)
def use_data():
    fopen=open('data.txt','r')
    for line in fopen:
        g = geocoder.google(line)
        ans=g.latlng
        if ans is not None:
            lats.append(ans[0])
            lans.append(ans[1])
    fopen.close()
    print(lats)
    print(lans)
    graph(lats,lans)

def graph(lats,lans):
    map_option=GMapOptions(lat=0,lng=0,zoom=3)
    plot=GMapPlot(x_range=Range1d(),y_range=Range1d(),map_options=map_option)
    plot.title.text='example'
    #plot.api_key='AIzaSyDg82cXIhKEGCTYt2XtWZhp6r5EuJbB94E'
    plot.api_key='AIzaSyAtt_C5_5WTwW-0bTHYi4aSDmURoU1UzvE'
    source=ColumnDataSource(data=dict(lat=lats,lon=lans))
    circle=Circle(x='lon',y='lat',size=15,fill_color='red',fill_alpha=0.6)
    plot.add_glyph(source,circle)
    plot.add_tools(PanTool(),WheelZoomTool(),BoxSelectTool())
    output_file('google.html')
    show(plot)
if open('data.txt'):
    use_data()
else:
    get_data()