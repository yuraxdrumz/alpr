import os
from sklearn.externals import joblib

def load_model():
    # load the model
    current_dir = os.path.dirname(os.path.realpath(__file__))
    model_dir = os.path.join(current_dir, 'models/svc/svc.pkl')
    model = joblib.load(model_dir)
    return model


def predict_characters(model, characters):
    classification_result = []
    for each_character in characters:
        # converts it to a 1D array
        each_character = each_character.reshape(1, -1);
        result = model.predict(each_character)
        classification_result.append(result)
    return classification_result

def first_item_in_sub_array_to_combined_string(arr):
    string = ''
    for each in arr:
        string += each[0]  
    return string  

def array_sort(arr, compare_string):
    copy = arr[:]
    arr.sort()
    string = ''
    for each in arr:
        string += compare_string[copy.index(each)]    
    return string

def iterate_found_plates(plates, column_lists):
    found = []
    model = load_model()
    for idx, characters in enumerate(plates):
        predict_array = predict_characters(model, characters)
        string_result = first_item_in_sub_array_to_combined_string(predict_array)
        sorted_predict_array = array_sort(column_lists[idx], string_result)
        found.append(sorted_predict_array)
    return found