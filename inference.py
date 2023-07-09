import joblib
import pandas as pd
import json
import numpy as np

class InferencePipeline:
    def __init__(self, feature_creator, model_path='assets/tagging_model.pkl'):
        self.feature_creator = feature_creator
        self.model = joblib.load(model_path)

    def preprocess_input(self, json_string):
        # Convert the JSON string to a dictionary
        data_dict = json.loads(json_string)
        # Convert the dictionary to a DataFrame
        inference_df = pd.DataFrame(data_dict)

        # Preprocess the DataFrame using the feature_creator
        preprocessed_df = self.feature_creator.get_data_for_inference(inference_df)

        return preprocessed_df

    def predict(self, json_string):
        # Preprocess the input
        preprocessed_df = self.preprocess_input(json_string)

        # Make a prediction using the model
        prediction = self.model.predict_proba(preprocessed_df)
        # Sort By values
        top_three = np.argsort(prediction, axis=1)[:, -3:]
        top_three_labels = np.array([self.model.classes_[i] for i in top_three])
        top_three_probs = np.sort(prediction, axis=1)[:, -3:]
        top_three_with_probs = [sorted(zip(labels, probs), key=lambda x: x[1], reverse=True) for labels, probs in zip(top_three_labels, top_three_probs)]
        return top_three_with_probs
