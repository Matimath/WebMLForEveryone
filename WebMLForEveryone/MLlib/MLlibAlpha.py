import pandas as pd
import numpy
from enum import Enum
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
                raise ValueError("No valid variable column")
            self.data = data
        except:
            self.is_valid = 0

    def train_model(self, selected_model):
        try:
            if selected_model == Selected_model.LINEAR_REGRESION or selected_model == Selected_model.LINEAR_REGRESION.name:
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
        return self.get_model().predict([self.translate_vector(vec)]).tolist()[0]

    def predict_from_data(self, data, column_index):
        predictions = []
        for row in data:
            del row[column_index]
            empty_row = False
            for i, cell in enumerate(row):
                if cell == "null":
                    empty_row = True
                if self.value_type[i] == Data_type.NUMBER:
                    try:
                        row[i] = float(cell)
                    except:
                        empty_row = True
            if not empty_row:
                predictions.append(self.predict(row))
            else:
                predictions.append("")
        return predictions

    def predict_from_file(self, path_in, path_out):
        data = get_excel_data(path_in)
        columns = get_columns(path_in)

        column_index = len(columns) - 1
        for i, col in enumerate(columns):
            if col == self.target_column:
                column_index = i
                break

        for row in data:
            del row[column_index]
            # TODO validate row
            pred = self.predict(row)
            row.insert(column_index, pred)

        save_to_excel(data, columns, path_out)


def get_columns(path):
    with pd.ExcelFile(path) as xls:
        data = pd.read_excel(xls, xls.sheet_names[0])
        return data.columns.values


def get_excel_data(path):
    with pd.ExcelFile(path) as xls:
        data = pd.read_excel(xls)
        return data.values.tolist()


def save_to_excel(data, columns, path):
    df = pd.DataFrame(data=data, columns=columns)
    writer = pd.ExcelWriter(path)
    df.to_excel(writer, 'Sheet1', index=False)
    writer.save()
