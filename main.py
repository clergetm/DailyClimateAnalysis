import os
import numpy as np

from Utils.Get import get_data, get_nan, get_duplicate

if __name__ == '__main__':
	file_path = "Files/DailyDelhiClimateTrain.csv"
	if not (os.path.isfile(file_path)):
		print("fichier manquant")
		exit()
		
	# Variables
	dataFrame = get_data(file_path, sep=',', txt=True)
	
	# Get information about duplicates and nan in the dataFrame
	# print("Nan")
	# print(get_nan(dataFrame))
	# print("duplicates")
	# print(get_duplicate(dataFrame))
	# There is no duplicates and no nan in this dataset
	