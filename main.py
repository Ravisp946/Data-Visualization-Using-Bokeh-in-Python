import pandas as pd

from os.path import dirname,join

from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from scripts.histogram import histogram_tab
from scripts.density import density_tab
from scripts.table import table_tab


flights=pd.read_csv(join(dirname(__file__),'data','flights.csv'),index_col=0).dropna()

map_data=pd.read_csv(join(dirname(__file__),'data','flights_map.csv'),header=[0,1],index_col=0)

tab1=histogram_tab(flights)
tab2=density_tab(flights)
tab3=table_tab(flights)
tabs=Tabs(tabs=[tab1,tab2,tab3])

curdoc().add_root(tabs)