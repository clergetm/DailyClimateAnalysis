import pandas as pd
import numpy as np
import datetime
from dateutil import parser
from scipy import stats


def get_data(path, sep=',', header=0, txt=True) -> pd.DataFrame:
	"""
	Create the dataframe from the csv and print some information about it
	:param str path: the path to the csv file
	:param char sep: the separation character
	:param int header: the row where the columns names are
	:param bool txt: True to execute all print in this function
	:return: the dataframe of the csv
	:rtype: pd.DataFrame
	"""
	data = pd.read_csv(path, sep=sep, header=header)
	
	# Get the shape of the data
	data_shape = data.shape
	if txt:
		print("\nShapes")
		print(f"There is {str(data_shape[0])} instances and {str(data_shape[1])} features")
		
		# print the features names of the dataset
		print("\nFeatures : ")
		for column_name in data.columns:
			print(f" - {column_name}")
	
	return data


def get_class(df, year) -> pd.DataFrame:
	"""
	Get class of the dataFrame depend to class_id and the year
	:param pd.DataFrame df: the data frame used
	:param int year: the year in which we focus
	:return: the dataFrame containing data from the year only
	:rtype: pd.DataFrame
	"""
	# Creating a mask between the start and the end of the year
	mask = (df.index >= str(year - 1) + "-12-31") & (df.index < str(year + 1) + "-01-01")
	return df.loc[mask]


def get_nan(df, on="dataframe") -> np.ndarray:
	"""
	Get all the row which got Nan values
	:param pd.DataFrame df: the data frame used
	:param str on: the type of element the function will be on
	:return: The Dataframe with row that got NaN values
	:rtype: pd.DataFrame
	"""
	res = pd.DataFrame()
	if df.isnull().values.any():
		if on == "dataframe":
			# get the row is a Nan value is found anywhere in the dataframe
			res = df[df.isnull().any(axis=1)]
		else:
			# get the row is a Nan value is found in this column
			res = df[df[on].isna()]
	return res


def get_duplicate(df, on="dataframe", keep=False) -> pd.DataFrame:
	"""
	Get all duplicated rows
	:param pd.DataFrame df: the data frame used
	:param str on: the type of element the function will be on
	:param bool keep: keep parameters for duplicated function
		keep means that all duplicated row will be return
	:return: the dataframe with all duplicated values
	:rtype: pd.DataFrame
	"""
	if on == "dataframe":
		return df[df.duplicated(keep=keep)]
	else:
		# Obtains duplicate row based on one column
		return df[df[on].duplicated(keep=keep)]


def get_specs(df, signal, dates, time_window_length, non_overlapping_length):
	"""
	Get a dataframe with specifications calculated
	:param pd.DataFrame df: the dataframe used
	:param str signal: the column used as a signal
	:param list dates: The two dates between which the values are taken
	:param int time_window_length: The number of date in one window
	:param int non_overlapping_length: The number of different dates between two window following each other
	:return pd.DataFrame: The dataframe of extracted specifications
	"""
	start = parser.parse(dates[0])  # Assuming that date[1] > date[0]
	end = parser.parse(dates[1])
	maximum = (end - start).days + 1  # The numbers of days +1 for the last day
	res_data = []
	feature_list = []
	y_data = []
	for i in range(0, maximum - time_window_length, non_overlapping_length):
		# Create the mask of dates
		first = start + datetime.timedelta(i)
		last = first + datetime.timedelta(time_window_length)
		mask = (df.index >= first) & (df.index < last)
		# Get a part of the dataframe that matches the mask
		slice_df = df[signal].loc[mask]
		
		# Get the specifications for this part
		vector_features, feature_list = get_all_specs(slice_df)
		res_data.append(vector_features)
		y_data.append(
			get_season(first.date()))
	# Get the seasons for this mask
	
	res_columns = [f"{feature}_{signal}" for feature in feature_list]
	return pd.DataFrame(res_data, columns=res_columns), y_data


def get_specs_min(df):
	"""
	Get the min value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the min value
	:rtype: float
	"""
	return np.min(df, axis=0)


def get_specs_max(df):
	"""
	Get the max value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the max value
	:rtype: float
	"""
	return np.max(df, axis=0)


def get_specs_mean(df):
	"""
	Get the mean value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the mean value
	:rtype: float
	"""
	return np.mean(df, axis=0)


def get_specs_std(df):
	"""
	Get the std value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the std value
	:rtype: float
	"""
	return np.std(df, axis=0)


def get_specs_skewness(df):
	"""
	Get the skewness value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the skewness value
	:rtype: float
	"""
	return stats.skew(df, axis=0)


def get_specs_kurtosis(df):
	"""
	Get the kurtosis value of the Dataframe
	:param pd.DataFrame df: the currently used DataFrame
	:return: the kurtosis value
	:rtype: float
	"""
	return stats.kurtosis(df, axis=0)


def get_all_specs(df):
	"""
	Get all specifications and their order
	:param pd.DataFrame df: the currently used DataFrame
	:return: specs, the array of all specs and a list of type of specs
	:rtype: (numpy.array,list)
	"""
	specs = get_specs_min(df)
	specs = np.append(specs, get_specs_max(df))
	specs = np.append(specs, get_specs_mean(df))
	specs = np.append(specs, get_specs_std(df))
	specs = np.append(specs, get_specs_skewness(df))
	specs = np.append(specs, get_specs_kurtosis(df))
	return specs, ["min", "max", "mean", "std", "skewness", "kurtosis"]


def get_season(target_date):
	"""
	Get the season of the given date
	:param datetime.date target_date:
	:return: the season
	:rtype: str
	"""
	year = target_date.year
	#           seasons :                   start,                                    end
	seasons = {"spring": [datetime.date(year=year, month=3, day=20), datetime.date(year=year, month=6, day=20)],
	           "summer": [datetime.date(year=year, month=6, day=21), datetime.date(year=year, month=9, day=21)],
	           "autumn": [datetime.date(year=year, month=9, day=22), datetime.date(year=year, month=12, day=20)],
	           # "winter": [datetime.date(year=year, month=12, day=21), datetime.date(year=year, month=12, day=31)],
	           # "winter": [datetime.date(year=year, month=1, day=1), datetime.date(year=year, month=3, day=19)]
	           }

	for i in range(0, len(seasons)):
		start, end = list(seasons.values())[i]
		
		# If we are in the the same month as a starting month of a season
		if start.month == target_date.month:
			# We check the date in that case
			# If the target day is superior or equal to the starting day of the starting month of a season
			if target_date.day >= start.day:
				# Return this season
				return list(seasons.keys())[i]
			# If the target day is inferior to the starting day of the starting month of a season
			else:
				# Return the precedent season
				return "winter" if i == 0 else list(seasons.keys())[i-1]
		# If we are between the starting and ending months of a season
		elif start.month < target_date.month < end.month:
			# Return this season
			return list(seasons.keys())[i]
		# If we are in the the same month as a ending month of a season
		elif end.month == target_date.month:
			# We check the date in that case
			# If the target day is superior or equal to the starting day of the starting month of a season
			if target_date.day <= start.day:
				# Return this season
				return list(seasons.keys())[i]
			# If the target day is superior to the starting day of the starting month of a season
			else:
				# Return the next season
				return list(seasons.keys())[i + 1] if i < 2 else "winter"

	# If not specifications found, then the date is a winter date
	return "winter"
