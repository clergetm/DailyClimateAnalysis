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
	
	:param pd.DataFrame df: the dataframe used
	:param str column_name: the column used to plot
	:param dates: The two dates between which the plot is made
	:param str dateformat: the dateformat for the horizontal axis
	:param list labels: labels contains the xlabel, the ylabel and the title of the plot
	:return:
	"""
	if dates is None:
		dates = ['2013-01-01', '2013-02-02']
	mask = (df.index >= dates[0]) & (df.index < dates[1])
	plot_time_series(df.loc[mask], column_name, dateformat, labels)
