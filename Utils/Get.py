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


def get_classes(df, class_id, var) -> dict:
	"""
	Get classes of the dataFrame depend to class_id and the var
	:param pd.DataFrame df: the data frame used
	:param np.ndarray class_id: the value used as classes
	:param str var: the variable in which we focus
	:return: classes, containing the indices of each id
	:rtype: dict
	"""
	
	classes = {}
	
	for id_value in class_id:
		indices = np.where(df[var] == id_value)
		# print(indices.shape[2])  # Number of element in each array
		classes[id_value] = indices[0]  # Add the indices to the dictionary
	
	return classes


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
