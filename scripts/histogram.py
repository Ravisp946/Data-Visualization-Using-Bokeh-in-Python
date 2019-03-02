import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource,Panel, FuncTickFormatter,SingleIntervalTicker,LinearAxis

from bokeh.models.widgets import CheckboxGroup,Slider,RangeSlider,Tabs,CheckboxButtonGroup,TableColumn,DataTable,Select

from bokeh.layouts import column,row,WidgetBox
from bokeh.palettes import Category20_16


#Making Plot with Histogram and returning its tab

def histogram_tab(flights):

	def make_dataset(carrier_list,range_start=-60,range_end=120,bin_width=5):

		by_carrier=pd.DataFrame(columns=['proportion','left','right',
									'f_proportion','f_interval','name','color'])

		range_extent=range_end-range_start

		for i, carrier_name in enumerate(carrier_list):

			#subset to the carrier
			subset=flights[flights['name']==carrier_name]

			#create a hostogram
			arr_hist,edges=np.histogram(subset['arr_delay'],bins=int(range_extent/bin_width),range=[range_start,range_end])

			arr_df=pd.DataFrame({'proportion':arr_hist/np.sum(arr_hist),'left':edges[:-1],
				'right':edges[1:]})
			arr_df['f_proportion']=['%0.5f' % proportion for proportion in arr_df['proportion']]

			arr_df['f_interval']=['%d to %d minutes' % (left,right) for left,right in zip(arr_df['left'],arr_df['right']) ]

			#Assign the carrier for labels
			arr_df['name']=carrier_name

			arr_df['color']=Category20_16[i]

			by_carrier=by_carrier.append(arr_df)

		by_carrier=by_carrier.sort_values(['name','left'])

		return ColumnDataSource(by_carrier)

	def style(p):
		#Title
		p.title.align='center'
		p.title.text_font_size='20pt'
		p.title.text_font='serif'

		#Axis Titles
		p.xaxis.axis_label_text_font_size='14pt'
		p.xaxis.axis_label_text_font_style='bold'
		p.yaxis.axis_label_text_font_size='14pt'
		p.yaxis.axis_label_text_font_style='bold'

		#tick labels
		p.xaxis.major_label_text_font_size='12pt'
		p.yaxis.major_label_text_font_size='12pt'

		return p

	def make_plot(src):
		#Blank plot with correct labels
		p=figure(plot_width=700,plot_height=700,title='Histogram of Arrival Delays by Airline',
			x_axis_label='Delay(min)',y_axis_label='Proportion')

		#Quad glyphs to create a histogram
		p.quad(source=src,bottom=0,top='proportion',left='left',right='right',
			color='color',fill_alpha=0.7,hover_fill_color='color',legend='name',
			hover_fill_alpha=1.0,line_color='black')

		#Hover tool with vline mode
		hover = HoverTool(tooltips=[('Carrier', '@name'), 
									('Delay', '@f_interval'),
									('Proportion', '@f_proportion')],
						  mode='vline')

		p.add_tools(hover)

		#styling
		p=style(p)

		return p

	def update(arr,old,new):

		carrier_to_plot=[carrier_selection.labels[i] for i in carrier_selection.active]

		new_src=make_dataset(carrier_to_plot,
							range_start=range_select.value[0],
							range_end=range_select.value[1],
							bin_width=binwidth_select.value)

		src.data.update(new_src.data)

		# Carriers and Colors

	available_carriers=list(flights['name'].unique())
	available_carriers.sort()

	airline_colors=Category20_16
	airline_colors.sort()

	carrier_selection=CheckboxGroup(labels=available_carriers,active=[0,1])

	carrier_selection.on_change('active',update)

	binwidth_select=Slider(start=1,end=30,
								step=1,value=5,
								title='Bin Width(min)')

	binwidth_select.on_change('value',update)

	range_select=RangeSlider(start=-60,end=120,value=(-60,120),
									step=5,title='Range of Delays(min)')
	range_select.on_change('value',update)

	intitial_carriers=[carrier_selection.labels[i] for i in carrier_selection.active]

	src=make_dataset(intitial_carriers,range_start=range_select.value[0],range_end=range_select.value[1],bin_width=binwidth_select.value)

	p=make_plot(src)

	controls=WidgetBox(carrier_selection,binwidth_select,range_select)

	#create a row layout
	layout=row(controls,p)
	tab=Panel(child=layout,title='Histogram')

	return tab







