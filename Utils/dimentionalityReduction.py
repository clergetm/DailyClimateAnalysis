import os
import pickle

from sklearn.ensemble import ExtraTreesClassifier

########################################################################################################################
#                                                    USER PARAMETERS                                                   #
########################################################################################################################

# Define the path name of your .pickle file (dataset)
path_name = "../Files/Out/DailyDelhiClimate.pkl"

########################################################################################################################
#                                                   LOAD THE DATASET                                                   #
########################################################################################################################

# Load the dataset (you can modify the variables to be load. In this case, we have x an array of the features extracted
# for each instance and y a list of labels)
with open(path_name, 'rb') as file:
	x, y = pickle.load(file)
	
# Define the number of attribute to select
attribute_number_to_select = len(x.columns)


########################################################################################################################
#                                    REDUCE THE DIMENSIONALITY BY SELECTING FEATURES                                   #
########################################################################################################################

# Define the classifier
classifier_model = ExtraTreesClassifier(n_estimators=50)

# Train the classifier model to classify correctly the instances into the correct classes
classifier_model = classifier_model.fit(x, y)

# Get the score of importances for each attribute
importance_scores = classifier_model.feature_importances_

# Maintenant c'est a votre tour de coder le reste.
# Le reste doit extraire de x les N meilleurs attributs et afficher un rapport des attributs selectionnes par ordre
# croissant d'importances. Puis a la fin, vous sauvegarderez le nouveau dataset.

print(f"{x=} {y=}")
print(f"{classifier_model=}")
print(f"{importance_scores=}")