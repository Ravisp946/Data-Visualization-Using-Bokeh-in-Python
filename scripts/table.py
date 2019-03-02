import os
import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource,Panel
from bokeh.models.widgets import TableColumn,DataTable


def table_tab(flights):

	carrier_stats=flights.groupby('name')['arr_delay'].describe()
	# print(carrier_stats)
	carrier_stats=carrier_stats.reset_index().rename(
		columns={'name':'airline','count':'flights','50%':'median'})

	carrier_stats['mean']=carrier_stats['mean'].round(2)
	carrier_src=ColumnDataSource(carrier_stats)

	#Columns of table
	table_column=[TableColumn(field='airline',title='Airline'),
	TableColumn(field='flights',title='Number Of Flights'),
	TableColumn(field='min',title='Min Delay'),
	TableColumn(field='max',title='Max Delay'),
	TableColumn(field='median',title='Median Delay'),
	TableColumn(field='mean',title='Average Delay')
	]

	carrier_table=DataTable(source=carrier_src,columns=table_column,width=1000)

	tab=Panel(child=carrier_table,title='Summary Table')

	return tab

# flights=pd.read_csv(os.path.join(os.path.dirname(__file__),'data','flights.csv'),index_col=0).dropna()
# table_tab(flights)	