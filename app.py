# Import necessary libraries
from flask import Flask, request, jsonify
import feature_generator
import inference
import json

# Initialize a Flask application
app = Flask(__name__)

# Define a route for the API. This route will accept POST requests.
@app.route('/predict_tag', methods=['POST'])
def process_data():
    # Get the JSON data sent with the POST request
    data = request.get_json()
    
    # Extract 'users' and 'transactions' from the data. If they are not present, default to an empty list.
    users = data.get('users', [])
    transactions = data.get('transactions', [])

    # Initialize the feature creator and inference pipeline
    feature_generator_ = feature_generator.feature_creator(fpath_output='assets',inference=True)
    infer_pipe = inference.InferencePipeline(feature_creator=feature_generator_,model_path="assets/tagging_model.pkl")
    
    # Convert the users and transactions to a JSON string
    sample_transaction_json =json.dumps({"User":users,"Transaction":transactions})
    
    # Use the inference pipeline to make a prediction
    out = infer_pipe.predict(sample_transaction_json)
    
    # Create a response dictionary
    response = {'result': 'success', 'data': {"prob": out}}
    
    # Convert the response dictionary to a JSON response
    return jsonify(response)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=False)
