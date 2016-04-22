import pandas as pd
import numpy
from enum import Enum
from sets import Set
import re
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder


class Data_type(Enum):
	NUMBER = 1
	ENUM = 2
	IGNORE = 3


class Problem_type(Enum):
	ESTIMATION = 1
	CLASSIFICATION = 2
	IGNORE = 3


class Selected_model(Enum):
	LINEAR_REGRESION = 1


def is_number(row):
	for elem in row:
		if not isinstance(elem, int) and not isinstance(elem, float):
			return 0
	return 1


def is_enum_proportion(enum_size, vector_size):
	return 1


class ModelBuilder:
	is_valid = 1
	file_path = ""
	target_column = ""
	value_type = []
	translate_model = dict()
	X = []
	Y = []
	data = []
	model_type = 0
	model = 0

	def __init__(self, path, target_col):
		try:
			self.file_path = path
			if path == "":
				raise ValueError("No path in argument")
			self.target_column = target_col
			self.model_type = Problem_type.IGNORE

			# We download the data from excel file
			with pd.ExcelFile(path) as xls:
				data = pd.read_excel(xls, xls.sheet_names[0])
				if target_col not in data.columns.values:
					raise ValueError("Column you want to predict does not exist")

			# Gaining info about columns data type
			for column in data.columns.values:
				if is_number(data[column]):
					if column != self.target_column:
						self.value_type.append(Data_type.NUMBER)
						self.X.append(data[column].values)
					else:
						self.Y = data[column].values
						self.model_type = Problem_type.ESTIMATION
				else:
					if column != self.target_column:
						lb = preprocessing.LabelBinarizer()
						lb.fit(data[column].values)
						tr_data = lb.transform(data[column].values)
						if is_enum_proportion(lb.classes_.size, tr_data.shape[1]):
							for col in tr_data.transpose():
								self.X.append(col)
							self.translate_model[column] = lb
							self.value_type.append(Data_type.ENUM)
						else:
							self.value_type.append(Data_type.IGNORE)
					
					else:
						l = LabelEncoder()
						l.fit(data[column].values)
						self.Y.append(l.transform(data[column].values))
						self.model_type = Problem_type.CLASSIFICATION
						
			if self.model_type == 0:
				raise ValueError("Column you want to rpedict is neither numeric nor enum")
			if not (Data_type.NUMBER in self.value_type or Data_type.ENUM in self.value_type):
				raise exception("No valid variable column")
			self.data = data
		except:
			self.is_valid = 0
			
	def train_model(self, selected_model):
		try:
			if selected_model == Selected_model.LINEAR_REGRESION:
				self.model = OneVsRestClassifier(linear_model.LogisticRegression())
				self.model.fit(numpy.transpose(numpy.asarray(self.X)), numpy.transpose(numpy.asarray(self.Y)))
		except:
			self.is_valid = 0

	def get_model(self):
		return self.model

	def translate_vector(self, vec):
		i = 0
		result = []
		for column in self.data.columns.values:
			if column != self.target_column:
				if self.value_type[i] == Data_type.NUMBER:
					result.append(vec[i])
				elif self.value_type[i] == Data_type.ENUM:
					temp_list = self.translate_model[column].transform([vec[i]])
					for elem in temp_list:
						result.append(elem)
				i += 1
			
		return result

	def predict(self, vec):
		return(self.get_model().predict([x.translate_vector(vec)]))


def get_columns(path):
	with pd.ExcelFile(path) as xls:
		data = pd.read_excel(xls, xls.sheet_names[0])
		return data.columns.values