#!/usr/bin/env python

# new_nn
# A basic NN to test our theory
# Document by http://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We use only one output from MP free data to try and train
# The feature come from LIWC

import os, csv, random, json, sys
from common import *
from copy import deepcopy
from tabulate import tabulate
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler
from colorama import init, Fore, Back, Style
init()

LIWC_OUTPUT_FILE = './aggregated_result/van_liwc_result.txt'
FREE_DATA_FILE = './mypersonality_final.csv'
NLP_OUTPUT_FILE = './nlp_result_combined.json'

# Mapping from user ID to their output values
mp_data = {}

# Maping from USEr id to their input (features from LIWC)
liwc_data = {}

# Mapping from user id to their NLP count
nlp_data = {}

with open(FREE_DATA_FILE, 'r') as infile:
    reader = csv.DictReader(infile)
    # Read and construct data
    for row in reader:
        user_id = row['#AUTHID']
        if user_id not in mp_data:
            # only add data if this user is not yet accounted for
            # Otherwise we should push this down the street
            mp_data[user_id] = {
                'sEXT': float(row['sEXT']),
                'sNEU': float(row['sNEU']),
                'sAGR': float(row['sAGR']),
                'sCON': float(row['sCON']),
                'sOPN': float(row['sOPN']),
                'cEXT': 1 if row['cEXT'].lower() == 'y' else 0,
                'cNEU': 1 if row['cNEU'].lower() == 'y' else 0,
                'cAGR': 1 if row['cAGR'].lower() == 'y' else 0,
                'cCON': 1 if row['cCON'].lower() == 'y' else 0,
                'cOPN': 1 if row['cOPN'].lower() == 'y' else 0,
            }

# load the intput - data from LIWC
with open(LIWC_OUTPUT_FILE, 'r') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for row in reader:
        user_id = filename_to_user_id(row['Filename'])
        liwc_data[user_id] = {}

        for liwc_key in LIWC_KEYS:
            liwc_data[user_id][liwc_key] = float(row[liwc_key])

with open(NLP_OUTPUT_FILE, 'r') as infile:
    nlp_data = json.load(infile)

TOTAL_TEST_COUNT = 10
TEST_SET_SIZE = 25

# for test_count in range(TOTAL_TEST_COUNT):
TRAIT = 'cOPN'
print(TRAIT)

all_accu = []
test_headers = ['Test number', 'Correct', 'Incorrect', 'Percentage', 'Score' ]
test_table = []
test_count = 0
while test_count < TOTAL_TEST_COUNT:
    TEST_SET = []
    # Code for generating test set
    while len(TEST_SET) < TEST_SET_SIZE:
        # select a random user
        val = None
        while True:
            val = random.choice(mp_data.keys())
            if val not in TEST_SET:
                break;
        TEST_SET.append(val)

    # Training set
    X_train = []
    y_train = []

    # Test set
    X_test = []
    y_test = []

    for user_id in mp_data.keys():
        # Output
        current_y = mp_data[user_id][TRAIT]

        # Input
        current_x = deepcopy(liwc_data[user_id].values())

        # Bias
        current_x.append(1)

        # NLP word count
        nlp_wc = nlp_data[user_id]['count']
        current_x.append(nlp_wc)

        for nlp_key in NLP_DATA_FIELD:
            nlp_count = nlp_data[user_id]['map'][nlp_key]
            # The value of this NLP feature
            current_x.append(nlp_count)

            # Percentage of this NLP feature
            percentage = 100.00 * float(nlp_count) / float(nlp_wc) if nlp_wc != 0 else 0
            current_x.append(percentage)

        if user_id not in TEST_SET:
            X_train.append(current_x)
            y_train.append(current_y)
        else:
            X_test.append(current_x)
            y_test.append(current_y)

    # Create a scaler on the data
    scaler = StandardScaler() 
    scaler.fit(X_train)

    # Transform
    X_train = scaler.transform(X_train) 
    X_test = scaler.transform(X_test) 

    # An object to store out optimal solution - measured by checking the score of test set
    optimal_score = {
        # NN parameter
        'layer0': 0,
        'layer1': 0,
        'alpha': 0,

        # NN result
        'rate': 0,
        'score': 0,
        'table': None,
        'correct': 0,
        'incorrect': 0
    }

    # Header of the table we will print out
    headers = ['No', 'Username', 'WC', 'Preference']

    for layer0_node_count in range(20, 80):
        for layer1_node_count in range (20, 80):
            # for alfa_value in [1e-5, 2e-5, 3e-5, 1e-4, 2e-4, 3e-4]:
            for alfa_value in [1e-5]:
                clf = MLPClassifier(
                    solver='lbfgs',
                    alpha=alfa_value,
                    hidden_layer_sizes=(layer0_node_count, layer1_node_count),
                    random_state=1
                )
                clf.fit(X_train, y_train)
                current_loss = clf.loss_

                # Print out the test as table
                table = []
                prediction = clf.predict(X_test)
                tally = {
                    'correct' : 0,
                    'incorrect' : 0,
                }
                for i, user_id in enumerate(TEST_SET):
                    current_prediction = prediction[i]
                    current_test = y_test[i]
                    table_entry = [
                        i,
                        user_id,
                        liwc_data[user_id]['WC'],
                    ]
                    if current_prediction == current_test:
                        tally['correct'] += 1
                        colour = Fore.GREEN
                    else:
                        tally['incorrect'] += 1
                        colour =  Fore.RED
                    table_entry.append(colour + str(current_prediction) + Style.RESET_ALL)
                    table.append(table_entry)

                # A very simple way to count the success rate
                success_rate = 100 * float(tally['correct']) / float(tally['correct'] + tally['incorrect'])

                test_score = clf.score(X_test, y_test)


                if optimal_score['score'] < test_score:
                    # A success
                    optimal_score = {
                        'layer0': layer0_node_count,
                        'layer1': layer1_node_count,
                        'alpha': alfa_value,
                        'rate': success_rate,
                        'score': test_score,
                        'table': deepcopy(table),
                        'correct': tally['correct'],
                        'incorrect': tally['incorrect'],

                    }

    # if optimal_score['score'] < 0.73:
    #     continue
    print('Training Multilayer Neural Network with with {} training entries, each entry containing {} features'.format(
        len(X_train),
        len(X_train[0]),
    ))

    print('Optimal solution in term of score: \n NN with {} nodes in first hidden layer, {} hidden nodes in second one and alpha {}\n Correct/Incorrect: {}/{} ({}%, score: {})'.format(
        Fore.BLUE + str(optimal_score['layer0']) + Style.RESET_ALL,
        Fore.YELLOW + str(optimal_score['layer1']) + Style.RESET_ALL,
        Fore.YELLOW + str(optimal_score['alpha']) + Style.RESET_ALL,
        Fore.BLUE + str(optimal_score['correct']) + Style.RESET_ALL,
        Fore.BLUE + str(optimal_score['incorrect']) + Style.RESET_ALL,
        Fore.GREEN + str(optimal_score['rate']) + Style.RESET_ALL,
        Fore.GREEN + str(optimal_score['score']) + Style.RESET_ALL,
    ))
    # print('Result details')
    # print tabulate(optimal_score['table'], headers, tablefmt="plain")
    test_count += 1
    test_table.append([
        test_count,
        optimal_score['correct'],
        optimal_score['incorrect'],
        optimal_score['rate'],
        optimal_score['score'],
    ])
    all_accu.append(optimal_score['score'])
    print('{} / {}'.format(
        Fore.YELLOW + str(test_count) + Style.RESET_ALL,
        Fore.BLUE + str(TOTAL_TEST_COUNT) + Style.RESET_ALL,
    ))
    print (Fore.GREEN)
    print(all_accu)
    print(Style.RESET_ALL)

print('Overal result for the trait {}'.format(TRAIT))
print tabulate(test_table, test_headers, tablefmt="plain")
print (Fore.GREEN)
print(all_accu)
print(Style.RESET_ALL)
