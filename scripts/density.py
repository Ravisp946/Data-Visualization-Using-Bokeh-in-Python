import pandas as pd
import numpy as np

from scipy.stats import gaussian_kde

from bokeh.plotting import figure
from bokeh.models import CategoricalColorMapper, HoverTool, ColumnDataSource,Panel, FuncTickFormatter,SingleIntervalTicker,LinearAxis

from bokeh.models.widgets import CheckboxGroup,Slider,RangeSlider,Tabs,CheckboxButtonGroup,TableColumn,DataTable,Select

from bokeh.layouts import column,row,WidgetBox
from bokeh.palettes import Category20_16

def density_tab(flights):

	#create 3 function make_dataset,make_plot and update
	def make_dataset(carrier_list,range_start,range_end,bandwidth):

		xs=[]
		ys=[]
		colors=[]
		labels=[]

		for i,carrier in enumerate(carrier_list):
			subset=flights[flights['name']==carrier]
			subset=subset[subset['arr_delay'].between(range_start,range_end)]

			kde=gaussian_kde(subset['arr_delay'],bw_method=bandwidth)

			#evenly space x values
			x=np.linspace(range_start,range_end,100)

			#evaluate pdf at every value of x
			y=kde.pdf(x)

			#Append the values to plot
			xs.append(list(x))
			ys.append(list(y))

			#Append the colors and label
			colors.append(airline_colors[i])
			labels.append(carrier)

		new_src=ColumnDataSource(data={'x':xs,'y':ys,'color':colors,'label':labels})

		return new_src

	def make_plot(src):

		p=figure(plot_width=700,plot_height=700,
				title='Density Plotof Arrival Delays by Airline',
				x_axis_label='Delay(min)',y_axis_label='Density')

		p.multi_line('x','y',color='color',legend='label',
					line_width=3,
						source=src)

		#Hover tool with next line policy

		hover=HoverTool(tooltips=[('Carrier','@label'),
									('Delay','$x'),
									('Density','$y')],
									line_policy='next')

		#Add the hover tool and stylind
		p.add_tools(hover)

		p=style(p)

		return p

	def update(attr,old,new):

		carriers_to_plot=[carrier_selection.labels[i] for i in carrier_selection.active]

		#If no bandwidth is selected, use the default value
		if bandwidth_choose.active==[]:
			bandwidth=None
		else:
			bandwidth=bandwidth_select.value

		new_src=make_dataset(carriers_to_plot,range_start=range_select.value[0],range_end=range_select.value[1],
							bandwidth=bandwidth)

		src.data.update(new_src.data)

	def style(p):

		#title	
		p.title.align='center'
		p.title.text_font_size='20pt'
		p.title.text_font='serif'

		#Axix titles	
		p.xaxis.axis_label_text_font_size='14pt'
		p.xaxis.axis_label_text_font_style='bold'
		p.yaxis.axis_label_text_font_size='14pt'
		p.yaxis.axis_label_text_font_style='bold'

		return p

	#carriers and colors
	available_carriers=list(flights['name'].unique())
	available_carriers.sort()

	airline_colors=Category20_16		
	airline_colors.sort()

	#carrier to plot
	carrier_selection=CheckboxGroup(labels=available_carriers,active=[0,1])
	carrier_selection.on_change('active',update)

	range_select=RangeSlider(start=-60,end=180,value=(-60,120),step=5,
							title='Range of Delays')
	range_select.on_change('value',update)

	#Bandwidth of Kernel
	bandwidth_select=Slider(start=0.1,end=5,step=0.1,value=0.5,title='Bandwidth for density plot')

	bandwidth_select.on_change('value',update)

	#whether to set the bandwidth or have it done automatically
	bandwidth_choose=CheckboxGroup(labels=['Choose Bandwidth(Else Auto)'],active=[])
	bandwidth_choose.on_change('active',update)

	#Initial Carriers 
	initial_carrier=[carrier_selection.labels[i] for i in carrier_selection.active]
	#MAke the density data source
	src=make_dataset(initial_carrier,
					range_start=range_select.value[0],range_end=range_select.value[1],
					bandwidth=bandwidth_select.value)

	p=make_plot(src)

	p=style(p)

	#put controls in a single element
	controls=WidgetBox(carrier_selection,range_select,bandwidth_select,bandwidth_choose)

	#Create a row layout
	layout=row(controls,p)

	#Make a tab with the layout
	tab=Panel(child=layout,title='Density Plot')

	return tab



			

