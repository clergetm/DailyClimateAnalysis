import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
from matplotlib.ticker import AutoMinorLocator


def plot_time_series(df, column_name, dateformat="%y-%m-%d", labels=None):
	"""
	Plot the given dataframe with time series as index
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	"""
	# if no labels are given
	if labels is None:
		labels = ["x", "y", "title"]
	
	# Create the plot
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
	
	# Create the two limit dates
	date1 = f"{year}-{month}-01"
	date2 = f"{year}-{month + 1}-01"
	plot_between_dates(df=df, column_name=column_name, dates=[date1, date2], dateformat=dateformat, labels=labels)


def plot_between_dates(df, column_name, dates=None, dateformat="%y-%m-%d", labels=None):
	"""
	The two dates between which the plot is made
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param list dates: The two dates between which the plot is made
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	"""
	# if no dates are given
	if dates is None:
		dates = ['2013-01-01', '2013-02-02']
	mask = (df.index >= dates[0]) & (df.index < dates[1])
	plot_time_series(df.loc[mask], column_name, dateformat, labels)


def plot_time_slider(df, column_name, dates, block, step, title, time_slider_path):
	"""
	Plot the whole time slider between two dates
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param list dates: The two dates between which the plot is made
	:param int block: the number of date in one subplot
	:param int step: the number of different dates between two subplots following each other
	:param str title: the title of the plot
	:param str time_slider_path: The folder where the plots will be saved
	"""
	import datetime
	from dateutil import parser
	import os
	import glob

	# Get all variables needed
	start = parser.parse(dates[0])  # Assuming that date[1] > date[0]
	end = parser.parse(dates[1])
	maximum = (end - start).days + 1  # The numbers of days +1 for the last day
	
	# Create the plot
	# For y ticks on each plot we need the max and min value of 'column_name'
	# And no need to do this calculation every time
	y_maximum = df[column_name].max()
	y_minimum = df[column_name].min()
	for i in range(0, maximum - block, step):
		fig, ax = plt.subplots(figsize=(20, 10))
		first = start + datetime.timedelta(i)
		last = first + datetime.timedelta(block)
		mask = (df.index >= first) & (df.index < last)
		slice_df = df.loc[mask]
		ax.plot(slice_df.index.values,
		        slice_df[column_name].values,
		        'bo-')
		
		# Manage x and y parameters
		ax.set_title(title +
		             f" between {str(first.strftime('%Y-%m-%d'))} and {str(last.strftime('%Y-%m-%d'))}",
		             fontsize=16)
		# Ideas from https://stackoverflow.com/questions/66169989/ensuring-first-and-last-date-ticks-in-x-axis-matplotlib
		# Create list of daily ticks made of timestamp objects
		daily_ticks = [timestamp[1] for timestamp in enumerate(slice_df.index)]
		# Create the ticks for the plot, values range from 3 to 3 and always have the last value as ticks too
		ticks = np.unique(np.append(daily_ticks[::3], daily_ticks[-1]))
		# Create tick labels from tick timestamps
		labels = [timestamp.strftime('%m-%d') for idx, timestamp in enumerate(ticks)]
		
		# Manage x labels
		ax.set_xticks(ticks)
		ax.set_xticklabels(labels)
		ax.set_xlim(first, last)
		ax.tick_params(axis="x", direction="in", labelrotation=45)
		ax.xaxis.grid(color="grey", linestyle="dashed")  # vertical lines
		
		# Manage y labels
		ax.set_ylim(y_minimum, y_maximum)
		ax.tick_params(axis="y", direction="inout")
		ax.grid(axis="y", color="black", alpha=.5, linewidth=.5)
		ax.yaxis.set_minor_locator(AutoMinorLocator())
		
		# Save the plot
		plt.savefig(
			time_slider_path + "/" + f"plot_{column_name}_{(start + datetime.timedelta(i)).strftime('%Y_%m_%d')}--"
			                         f"{(last - datetime.timedelta(1)).strftime('%Y_%m_%d')}" + ".png")
		plt.close(fig)
