import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from sklearn.ensemble import ExtraTreesClassifier


def dim_reduc_protocol(pickle_filepath, plot_file_name):
	"""
	Execute the dimensionality reduction protocol to the given pickle file
	:param str pickle_filepath: The pickle file
	:param str plot_file_name: The name given to each plot created
	"""
	####################################################################################################################
	#                                                 LOAD THE DATASET                                                 #
	####################################################################################################################
	
	# Load the dataset (you can modify the variables to be load. In this case, we have x an array of the features extracted
	# for each instance and y a list of labels)
	with open(pickle_filepath, 'rb') as file:
		x, y = pickle.load(file)
	
	# Define the number of attribute to select
	attribute_number_to_select = int(len(x.columns) / 2)
	
	####################################################################################################################
	#                                  REDUCE THE DIMENSIONALITY BY SELECTING FEATURES                                 #
	####################################################################################################################
	
	# Define the classifier
	classifier_model = ExtraTreesClassifier(n_estimators=50)
	
	# Train the classifier model to classify correctly the instances into the correct classes
	classifier_model = classifier_model.fit(x, y)
	
	# Get the score of importances for each attribute
	importance_scores = classifier_model.feature_importances_
	
	# Maintenant c'est a votre tour de coder le reste.
	# Le reste doit extraire de x les N meilleurs attributs et afficher un rapport des attributs selectionnes par ordre
	# croissant d'importances. Puis a la fin, vous sauvegarderez le nouveau dataset.
	
	# Sort the features importances and get the ordered indices
	indices = np.argsort(importance_scores)[::-1]
	# Get the best features according to the reduction algorithm
	columns_to_select = x.columns[indices[0:attribute_number_to_select]]
	# Get the new dataset with the selected features
	new_dataset = x[columns_to_select]
	
	#  Plot the results
	plt.bar(x=np.arange(attribute_number_to_select), height=importance_scores[indices[0:attribute_number_to_select]],
	        tick_label=columns_to_select)
	
	plt.title(f"Feature Importances - Sum = {str(np.sum(importance_scores[indices[0:attribute_number_to_select]]))}")
	plt.xlabel(f"Selected features")
	plt.xticks(rotation=90)
	plt.ylabel(f"Importance score")
	plt.tight_layout()
	
	# Save the results
	plot_path = "../Files/Out/Plots/"
	if os.path.isfile(plot_path + plot_file_name):
		os.remove(plot_path + plot_file_name)
	plt.savefig(plot_path + plot_file_name + ".png")
	
	# Show the results
	plt.show()
	plt.close()
	
	# Save the dataset as Pickle file
	pickle_filepath = "../Files/Out/Pickles/"
	
	with open(os.path.join(pickle_filepath, plot_file_name + ".pickle"), "wb") as f:
		pickle.dump([new_dataset, y], f)


if __name__ == '__main__':
	dim_reduc_protocol("../Files/Out/Pickles/DailyDelhiClimate1.pkl", "DimReduction30-7")
	dim_reduc_protocol("../Files/Out/Pickles/DailyDelhiClimate2.pkl", "DimReduction20-5")
