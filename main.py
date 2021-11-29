import os
import pickle
import time

import pandas as pd

from Utils.Get import get_data, get_nan, get_duplicate, get_specs, get_y_data
from Utils.Graphics import plot_time_slider


def protocol(df, dates, time_window_length, non_overlapping_length, pickle_file, time_slider_path):
	"""
	The protocol of the subject
	:param pd.DataFrame df: the used DataFrame
	:param list dates: list of 2 elements : the bounds
	:param int time_window_length: the length of the window
	:param int non_overlapping_length: the number of non overlapping element
	:param str pickle_file: name of the pickle file, will be saved in "/Files/Out/Pickles"
	:param str time_slider_path: The folder where the plots will be saved
	"""
	import glob
	# Variables
	start_time = time.time()
	df_specs = pd.DataFrame()
	pickle_filepath = "/Files/Out/Pickles/" + pickle_file

	# files = glob.glob(time_slider_path + "/*")
	# for f in files:
	# 	os.remove(f)
	#
	# Get the specifications of each column
	for column_name in df.columns:
		# plot_time_slider(df, column_name, dates,
		# time_window_length, non_overlapping_length, f"TimeSlider of {column_name}",time_slider_path)
		# The y_data is changed every time but we only need as many y_data value as the number of row in the dataframe
		# So no extend, no append etc
		df_temp = get_specs(df, column_name, dates, time_window_length, non_overlapping_length)
		df_specs = pd.concat([df_specs, df_temp], axis=1)
	y_data = get_y_data(dates, time_window_length, non_overlapping_length)
	# Remove the file in order to create a fresh one
	if os.path.isfile(pickle_filepath):
		os.remove(pickle_filepath)
	
	with open("."+pickle_filepath, "wb") as f:
		pickle.dump([df_specs, y_data], f)
	
	end_time = time.time()
	print(f"total time = {end_time - start_time}")


if __name__ == '__main__':
	file_path_Train = "Files/DailyDelhiClimateTrain.csv"
	file_path_Test = "Files/DailyDelhiClimateTest.csv"
	if not (os.path.isfile(file_path_Train) and os.path.isfile(file_path_Test)):
		print("fichiers manquants")
		exit()
	
	# Creation and cleaning of variables
	dataFrame_Train = get_data(file_path_Train, sep=',', txt=False)
	dataFrame_Test = get_data(file_path_Test, sep=',', txt=False)
	
	# We concat all the data to have only one dataframe to use
	dataFrame = pd.concat([dataFrame_Train, dataFrame_Test], axis=0).reset_index(drop=True)
	del (dataFrame_Test, dataFrame_Train)
	
	# print("Get information about duplicates and nan in the dataFrame")
	# print("Nan: ")
	# print(get_nan(dataFrame))
	# print("Duplicates: ")
	# print(get_duplicate(dataFrame, 'date'))
	
	# There is one duplicate row :
	# this is the last row of Train dataset and the first of Test dataset.
	# We keep the row from Test dataset
	dataFrame.drop_duplicates(subset=['date'], keep='last', inplace=True)
	dataFrame = dataFrame.reset_index(drop=True)
	
	# change dtype of date from 'object' to 'datetime' and change the index
	dataFrame['date'] = pd.to_datetime(dataFrame['date'])
	dataFrame.set_index("date", inplace=True)
	
	# First time slider window
	protocol(dataFrame, dates=['2013-01-01', '2017-04-24'],
	         time_window_length=30, non_overlapping_length=7, pickle_file="DailyDelhiClimate1.pkl",
	         time_slider_path="Files/Out/TimeSlider/DimReduc1")

	# Second time slider window
	protocol(dataFrame, dates=['2013-01-01', '2017-04-24'],
	         time_window_length=20, non_overlapping_length=5, pickle_file="DailyDelhiClimate2.pkl",
	         time_slider_path="Files/Out/TimeSlider/DimReduc2")
	