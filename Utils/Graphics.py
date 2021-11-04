import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def plot_box_graphic(df, column_id, column_target):
	"""
	Create a box graphic of the column_id by the column_target
	:param pd.DataFrame df: the dataframe
	:param str column_id: the name of the class column
	:param str column_target: the name of the targeted column
	"""
	column_data = []
	class_id = np.unique(df[column_id])
	for id_value in class_id:
		indices = np.where(df[column_id] == id_value)
		column_data.append(df[column_target].values[indices])
	
	plt.boxplot(column_data, positions=class_id)
	plt.title(f"Distribution of {column_target}", fontsize=10)
	plt.xlabel(f"{column_id}")
	plt.ylabel(f"Level of {column_target} ")
	plt.show()


def plot_all_box(df, column_id):
	columns = df.columns.drop(labels=column_id)
	for i in range(len(columns)):
		plot_box_graphic(df, column_id, columns[i])


def plot_scatter_graphic(df, column_id, columns_targets):
	"""
	Create a scatter graphic
	Scatter plot is a useful method to see the correlation between 2 features
	:param pd.DataFrame df: the dataframe
	:param str column_id: the name of the class column
	:param list columns_targets: list of a coupe of targeted columns
	"""
	color_list = ["r", "g"]
	marker_list = ["o", "s"]
	class_id = np.unique(df[column_id])
	
	for id_value in class_id:
		column_data = []
		indices = np.where(df[column_id] == id_value)
		
		for column_name in columns_targets:
			column_data.append(df[column_name].values[indices])
		
		data_label = f"{column_id} | {str(id_value)}"
		
		plt.scatter(columns_targets[0], columns_targets[1], c=color_list[id_value], alpha=0.5,
		            marker=marker_list[id_value], edgecolor="k", label=data_label)  # o : circle
	plt.title(f"{columns_targets[0]} vs. {columns_targets[1]}", fontsize=10)
	plt.xlabel(f"{columns_targets[0]}")
	plt.ylabel(f"{columns_targets[1]}")
	plt.show()


def plot_all_scatter(df, column_id):
	columns = df.columns.drop(labels=column_id)
	for i in range(len(columns)):
		for j in range(len(columns)):
			if i > j:
				plot_scatter_graphic(df, column_id, [columns[i], columns[j]])


def plot_HeatMap_graphic(df):
	f, ax = plt.subplots(figsize=(15, 15))
	sns.heatmap(df.corr(), annot=True, linewidths=0.5, fmt='.1f', ax=ax)
	plt.show()