from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform
import os
from training_config import config
import joblib 
class Trainer:
    def __init__(self, feature_creator,fpath_output='./assets'):
        self.feature_creator = feature_creator
        self.fpath_output = fpath_output
        os.makedirs(self.fpath_output, exist_ok=True)

    def train(self):
        # Get the data
        X_train, X_test, y_train, y_test = self.feature_creator.get_data_for_training()

        # Initialize your classifiers with regularization
        # Using Bagging Technique with two classifiers
        svm = SVC(probability=True, C=config['svm_C'])
        gb = GradientBoostingClassifier(learning_rate=config['gb_learning_rate'], n_estimators=config['gb_n_estimators'], max_depth=config['gb_max_depth'], min_samples_split=config['gb_min_samples_split'])

        # Create a soft voting classifier
        voting_clf = VotingClassifier(estimators=[('svm', svm), ('gb', gb)], voting='soft')

        # Define a distribution of parameters to sample from
        param_distributions = {'svm__C': uniform(0.1, 10), 'gb__learning_rate': uniform(0.01, 1), 'gb__n_estimators': range(50, 150), 'gb__max_depth': range(3, 7), 'gb__min_samples_split': range(2, 6)}

        # Initialize a RandomizedSearchCV object
        random_search = RandomizedSearchCV(voting_clf, param_distributions, n_iter=config['random_search_n_iter'], cv=config['random_search_cv'], random_state=config['random_search_random_state'])

        # Train your classifier
        random_search.fit(X_train, y_train)

        # Print the best parameters
        print(random_search.best_params_)

        # Make predictions on your test set using the best model
        y_pred = random_search.predict(X_test)

        # Print a classification report
        report = classification_report(y_test, y_pred)

        print(report)

        # Save the classification report
        with open(os.path.join(self.fpath_output, 'classification_report.txt'), 'w') as f:
            f.write(report)
        # Save the model
        joblib.dump(random_search.best_estimator_, os.path.join(self.fpath_output,'tagging_model.pkl'))
