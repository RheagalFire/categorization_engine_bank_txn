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


