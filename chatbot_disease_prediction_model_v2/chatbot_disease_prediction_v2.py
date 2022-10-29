# Importing libraries
import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle
from pathlib import Path


# Reading the train.csv by removing the
# last column since it's an empty column
DATA_PATH = "data/Training.csv"
data = pd.read_csv(DATA_PATH).dropna(axis=1)

# Encoding the target value into numerical
# value using LabelEncoder
encoder = LabelEncoder()
data["prognosis"] = encoder.fit_transform(data["prognosis"])

X = data.iloc[:, :-1]
y = data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=24)

# Initializing Models
models = {
    "SVC": SVC(),
    "Gaussian NB": GaussianNB(),
    "Random Forest": RandomForestClassifier(random_state=18)
}

# Training the models on whole data
final_svm_model = SVC()
final_gnb_model = GaussianNB()
final_rf_model = RandomForestClassifier(random_state=18)


projectLocation = Path(__file__).absolute().parent
rf_model_file = 'rf_model.pkl'
gnb_model_file = 'gnb_model.pkl'
svm_model_file = 'svm_model.pkl'

rf_model_path = Path(f'{projectLocation}/prediction_model/{rf_model_file}')
gnb_model_path = Path(f'{projectLocation}/prediction_model/{gnb_model_file}')
svm_model_path = Path(f'{projectLocation}/prediction_model/{svm_model_file}')

if rf_model_path.exists():
    final_rf_model = pickle.load(open(rf_model_path, 'rb'))
else:
    final_rf_model.fit(X, y)
    pickle.dump(final_rf_model, open(rf_model_path, 'wb'))

if gnb_model_path.exists():
    final_gnb_model = pickle.load(open(gnb_model_path, 'rb'))
else:
    final_gnb_model.fit(X, y)
    pickle.dump(final_gnb_model, open(gnb_model_path, 'wb'))

if svm_model_path.exists():
    final_svm_model = pickle.load(open(svm_model_path, 'rb'))
else:
    final_svm_model.fit(X, y)
    pickle.dump(final_svm_model, open(svm_model_path, 'wb'))

symptoms = X.columns.values

# Creating a symptom index dictionary to encode the
# input symptoms into numerical form
symptom_index = {}
for index, value in enumerate(symptoms):
    symptom = " ".join([i.lower() for i in value.split("_")])
    symptom_index[symptom] = index

data_dict = {
    "symptom_index": symptom_index,
    "predictions_classes": encoder.classes_
}


# Defining the Function
# Input: string containing symptoms separated by commmas
# Output: Generated predictions by models
def predict_disease(input_symptom):
    input_symptom = input_symptom.split(",")

    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in input_symptom:
        symptom = symptom.lower()
        if symptom in data_dict['symptom_index']:
            index = data_dict["symptom_index"][symptom]
            input_data[index] = 1
        else:
            return "NO DATA"

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1, -1)

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][final_rf_model.predict(input_data)[0]]
    nb_prediction = data_dict["predictions_classes"][final_gnb_model.predict(input_data)[0]]
    svm_prediction = data_dict["predictions_classes"][final_svm_model.predict(input_data)[0]]

    # making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction, svm_prediction])[0][0]
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "svm_model_prediction": nb_prediction,
        "final_prediction": final_prediction
    }
    print(predictions)
    return final_prediction


# Testing the function
user_input = input("Enter disease sympton: ")
print(predict_disease(user_input))
