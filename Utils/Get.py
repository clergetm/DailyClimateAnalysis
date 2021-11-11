import pandas as pd
import numpy as np


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
	mask = (df.index >= str(year-1)+"-12-31") & (df.index < str(year+1)+"-01-01")
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
