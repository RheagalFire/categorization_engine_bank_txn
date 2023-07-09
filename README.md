# Categorization engine For bank transactions
This repository contains code and logic for building a categorization engine for bank transactions.

## Table of Contents 
- Synthetic Data Generation
- Cleaning the Transactional Query
- Embeddings/Features Creation
- Training Pipeline
- Inferencing Pipeline
- Deploying as an API endpoint
- Results

### Sythetic Data Generation
I took the sample schema of the dataset shared and created a synthetic data based on the same patern 
<p>Shared Sample Dataset</p>

![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/af790ae7-12bb-41a1-947b-f9ed59fb04b5)

<p>Synthetically Generated Dataset</p>

![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/0e8fde04-5da9-4052-a45c-0d6851f6d19d)

These configs for generating the are mentioned in the [config_data.py](config_data.py) file.
What it does is it takes in num_of_users and palces by tag mentioned in the config file and create random transactions for these users. 
Some things that are handled in the [generation function](utils.py).
- Loop over number of users mentioned in the config file
- Randomly Select a place for the transaction that hasn't been user for the user.
- Add random noise to the transaction like 'XXX' and transaction prefixes such as POS etc. Also add random alphanumeric chars.<br>

Dump this synthetic Data Created using [data_generator.py](data_generator.py).You can specify the output folder where you want to dump this.

### Cleaning the Transactional Query
- Remove Punctuations
- Remove alphanumeric chars
- Remove unnecesarry sequences of 'XXX'
- Remove transaction prefixes such as pos,mps,bil etc

Now this is custom way of doing cleaning of the transaction query where we want to remove all the noise from the data and want to focus just on the merchant.<br>
The results after doing this are : <br>
![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/3754a7b3-6a51-43a2-aae1-757b48528545)<br>
You can see we are able to reduce much of the noise. Still some of it are left.<br>

Just to experiment on new things i tried giving the transactional query to chatllm model to see if it can give me the exact merchant name.<br>
![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/1a752a4c-502a-4b20-abeb-89b93cc16cfb)<br>
The results were very impressive. The constraints to this approach would require us handling these things:
- How can we send in multiple transactional queries at one pass. (We will keep the context window in mind)
- Profile the time required to do so, what kind of latency are we looking at?
- Can we use a lighter parameter open source model, can we achieve similar results(because easier to deploy for custom use case).
- We can fine tune a base model for this task or prompt engineering with few shot examples would work for us.<br>

We need to answer the above questions before moving on to use this to extract merchant from the transaction. You can follow along this [notebook](notebooks/Merchant_Extraction_From_Langchain.ipynb) to see how to extract merchant from the transaction query using langchain and chatgpt.

### Embeddings/Features Creation
So to create our featureset, we are going to use embeddings to represent our transaction words into contextual vectors.(Similar words would have similar vector space)
Now for the purpose of this project i did not experimented with something large. 
What i kept in mind were these 
- Multillingual Embeddings
- Small Size of the embedding model
- Good Accuracy across the MTEB board
So I head over to the MTEB board to find such model and i ended up choosing <b>all-MiniLM-L6-v2</b>
![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/0e13af41-0383-47dc-b4bd-e2fb68cac40d) <br>

The chosen embedding model projects our transactions to a vector space of <b>384 dimensions</b> where we have used each dimension as a featureset.<br>

Head over to this [notebook](notebooks/2-Embeddings%20Creation.ipynb) to follow how i create embeddings from the transactional queries.

### Training Pipeline 
Training is kept quite simple because we are working with synthetic data. I have decided to go with <b>Bagging</b> Approach using `SVC` and `Gradient Boosting` Algo. I do a Randomized Search CV on hyperparameters to find out the best hyperparameter store the test results and model file in the assests folder. 
[trainer.py](trainer.py) is the module where you can find the code for training the model. 
Some of the things that i kept in mind while preparing the data for training : 
- Using user_id as a feature in itself. We want to add the past preferences by the user to increase the chances of tag prediction for that use.
- Split the train/test stratified on the user_id. We want to keep all the users in our training set as it is essential for our model to make predictions based on previous taggings.
- Since this data is synthetically created and for every user we have similar places and transactions (although with different noises),this model is definately going to overfit.<br>
![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/311ed93d-cc06-4fdf-b6c4-22260b860a59) <br>
This has clearly overfitted. (Because of common keywords for multiple users). But we are not benchmarking scores on synthetic data. It would make sense to do
so when we have large amount of actual transaction data.<br>.The training took approx <b>6 mins</b> to be completed. 
You can follow along this [notebook](notebooks/3-Training%20Pipeline.ipynb) to see how you can train on the synthetic data.

### Inferencing 
Inferencing is pretty simple, we use the same module [feature_generator.py](feature_generator.py) that was used at the time of the training but with the inference settings to create features.For the pipeline refer to this [inference pipeline](inference.py). At the time of the inferencing we 
- Preprocess/clean the data , the way we did at the time of the training.
- We check if the user is already in the userbase and the model was trained on the data by that user. If now we assign the user a value of -1.
- Predict out top three labels with probability score.<br>
  Follow this [notebook](notebooks/4-Inference.ipynb) to walkthrough how inferencing is done.
  
### Deploying as an API endpoint
I built a [flask app](app.py) around the inference module and [contanirized](Dockerfile) it for hosting it.<br>
I have used ECS service from AWS to host the Dockerimage. 
![image](https://github.com/RheagalFire/categorization_engine_bank_txn/assets/60213893/0de0f034-0f7b-4d83-8c88-e4243c28050c)<br>
Have used default scaling and security groups.

API ENDPOINT : http://13.233.3.50:8080/predict_tag

To send a sample request through CURL
```
curl -X POST http://13.233.3.50:8080/predict_tag -H "Content-Type: application/json" -d "{\"users\": [\"User200\", \"User3\"], \"transactions\":[\"POS XXXXXXXXXXXX1111 IKEA INDIA PVT L\", \"POS XXXXXXXXXXXX1111 APOLLO PHARMACY PVT L\"]}"
```
Output:
```
{"data":{"prob":[[["Shopping",0.6422143460736127],["Medical",0.18530665751017797],["Travel",0.11028613262101186]],[["Medical",0.9988152915012749],["Subscription",0.0006008496836324658],["Shopping",0.0004127586966547764]]]},"result":"success"}
```
### Results Comparision



