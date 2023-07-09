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

