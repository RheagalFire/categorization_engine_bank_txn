import os
import pickle
import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from utils import cleaning
import re

class feature_creator():
    def __init__(self, fpath_data_input='data/synthetic_data.csv', fpath_output='assets',inference=False):
        if (inference):
           self.inference = True
        else:
            self.synthetic_data = pd.read_csv(fpath_data_input)
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.fpath_output = fpath_output

    def preprocessing(self, data):
        # Apply the cleaning function to each Transaction in the DataFrame.
        data['Transaction'] = data['Transaction'].apply(lambda x:x.lower())
        data['Transaction'] = data['Transaction'].map(cleaning)
        # Create a translation table that maps every punctuation character to a space.
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        # Use the translation table to replace punctuation with spaces in each Transaction.
        data['Transaction'] = [x.translate(translator) for x in data['Transaction']]
        # Tokenize the Transaction by splitting it into words. Only keep the words that consist entirely of alphabetic characters.
        data['Transaction'] = data['Transaction'].map(lambda x: [word for word in x.split(' ') if word.isalpha()])
        # Join the words back together into a single string with spaces in between.
        data['Transaction'] = data['Transaction'].map(lambda x: ' '.join(x))
        return data

    def dump_users(self):
        # We maintain the list of users because we use user as a feature for the training dataset
        users_available = self.synthetic_data['User'].tolist()
        # Dump these Users
        with open(os.path.join(self.fpath_output,'users_available.pkl'), 'wb') as f:
            # Write the list to the file
            pickle.dump(users_available, f)

    def create_clean_embeddings(self, data,inferencing=False):
        sentences = data['Transaction'].to_list()
        embeddings = self.model.encode(sentences)
        embeddings_dataset = pd.concat([data, pd.DataFrame(embeddings)], axis=1)
        if(inferencing):
            with open(os.path.join(self.fpath_output,'users_available.pkl'), 'rb') as f:
                # Load the list from the file
                loaded_users_available = pickle.load(f)
            embeddings_dataset['User_id'] = embeddings_dataset['User'].apply(lambda x:x.replace('User','') if x in loaded_users_available else -1)
        else:
            # Replace User with '' to make it int
            embeddings_dataset['User_id'] = embeddings_dataset['User'].str.replace('User','')
        # Change the datatype of the UserId from string to the integer
        embeddings_dataset['User_id'] = embeddings_dataset['User_id'].astype(int)
        # Column names can't be of mixed datatype therefore change it to string 
        num_dimensions = 384
        column_mapping = {i: f'Feature{i}' for i in range(num_dimensions+1)}
        embeddings_dataset = embeddings_dataset.rename(columns=column_mapping)
        return embeddings_dataset

    def train_test_split(self, embeddings_dataset):
        # Prepare your featureset and the target variable
        X = embeddings_dataset.drop(columns=['Tag','User','Transaction'])
        y = embeddings_dataset['Tag']
        # Split your data into training and test sets using stratified split on the user_id. We want all users to be in the training set.
        # Will discuss why we want such a behaviour. 
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=embeddings_dataset['User_id'], random_state=42)
        return X_train, X_test, y_train, y_test

    def get_data_for_training(self):
        preprocessed_dataset = self.preprocessing(self.synthetic_data)
        self.dump_users()
        embeddings_dataset = self.create_clean_embeddings(preprocessed_dataset)
        X_train, X_test, y_train, y_test = self.train_test_split(embeddings_dataset)
        return X_train, X_test, y_train, y_test

    def get_data_for_inference(self, inference_df):
        inference_df = self.preprocessing(inference_df)
        embeddings_dataset = self.create_clean_embeddings(inference_df,inferencing=self.inference)
        return embeddings_dataset.drop(columns=['User','Transaction'])
