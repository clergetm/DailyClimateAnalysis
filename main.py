import os
import numpy as np
import pandas as pd
from Utils.Get import get_data, get_nan, get_duplicate, get_class

if __name__ == '__main__':
	file_path_Train = "Files/DailyDelhiClimateTrain.csv"
	file_path_Test = "Files/DailyDelhiClimateTest.csv"
	if not (os.path.isfile(file_path_Train) and os.path.isfile(file_path_Test)):
		print("fichiers manquants")
		exit()
		
	# Creation and cleaning of variables
	dataFrame_Train = get_data(file_path_Train, sep=',', txt=True)
	dataFrame_Test = get_data(file_path_Test, sep=',', txt=True)
	
	# We concat all the data to have only one dataframe to use
	dataFrame = pd.concat([dataFrame_Train, dataFrame_Test], axis=0).reset_index(drop=True)
	del(dataFrame_Test, dataFrame_Train)
	
	print("Get information about duplicates and nan in the dataFrame")
	print("Nan: ")
	print(get_nan(dataFrame))
	print("Duplicates: ")
	print(get_duplicate(dataFrame, 'date'))
	# There is one duplicate row :
	# this is the last row of Train dataset and the first of Test dataset.
	# Need to handle this
	
	# change dtype of date from 'object' to 'datetime'
	dataFrame['date'] = pd.to_datetime(dataFrame['date'])

	