import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import DateFormatter


def plot_time_series(df, column_name, dateformat="%y-%m-%d", labels=None):
	"""
	Plot the given dataframe with time series as index
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	"""
	if labels is None:
		labels = ["x", "y", "title"]
	fig, ax = plt.subplots(figsize=(12, 8))
	ax.plot(df.index.values,
	        df[column_name].values,
	        'bo-')
	ax.set(xlabel=labels[0],
	       ylabel=labels[1],
	       title=labels[2])
	
	date_form = DateFormatter(dateformat)
	ax.xaxis.set_major_formatter(date_form)
	plt.show()


def plot_month(df, column_name, year, month, dateformat, labels):
	"""
	Plot a whole month
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param int year: the targeted year
	:param int month: the targeted month
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	"""
	date1 = f"{year}-{month}-01"
	date2 = f"{year}-{month + 1}-01"
	plot_between_dates(df=df, column_name=column_name, dates=[date1, date2], dateformat=dateformat, labels=labels)


def plot_between_dates(df, column_name, dates=None, dateformat="%y-%m-%d",
                       labels=None):
	"""
	The two dates between which the plot is made
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param list dates: The two dates between which the plot is made
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	:return:
	"""
	if dates is None:
		dates = ['2013-01-01', '2013-02-02']
	mask = (df.index >= dates[0]) & (df.index < dates[1])
	plot_time_series(df.loc[mask], column_name, dateformat, labels)


def plot_time_slider(df, column_name, dates, block, i, title):
	"""
	Plot the whole time slider between two dates

	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param list dates: The two dates between which the plot is made
	:param int block: the number of date in one subplot
	:param int i: the number of different dates between two subplots following each other
	:param str title: the title of the plot
	"""
	import datetime
	from dateutil import parser
	from datetime import date
	import math
	
	# Get all variables needed
	max_col = 2
	start = parser.parse(dates[0])  # Assuming that date[1] > date[0]
	end = parser.parse(dates[1])
	maximum = (end - start).days  # The numbers of days between the two dates
	
	nb_subplot = math.ceil(maximum / block)  # How many subplot will be created
	nb_row_subplot = math.ceil(nb_subplot / max_col)  # How many row will be created for subplots
	
	# Create the plot

	for row in range(0, nb_row_subplot):
		fig, ax = plt.subplots(max_col)
		fig.subplots_adjust(hspace=2.5)
		fig.suptitle(title)
		for col in range(0, max_col):
			start += datetime.timedelta(col * i)
			last = start + datetime.timedelta(block) if start + datetime.timedelta(block) <= end else end
			mask = (df.index >= start) & (df.index < last)
			slice_df = df.loc[mask]
			ax[col].plot(slice_df.index.values,
			                  slice_df[column_name].values,
			                  'bo-')
			ax[col].tick_params(labelrotation=25)
		plt.show()
	
