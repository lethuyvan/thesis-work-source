#!/usr/bin/env python

# simple_nn
# A basic NN to test our theory
# Document by http://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We use only one output from MP free data to try and train
# The feature come from LIWC and POS

import os, csv, random, json, sys
from common import *
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from copy import deepcopy
init()

LIWC_OUTPUT_FILE = './crawled_result/van_liwc_result.txt'
FREE_DATA_FILE = './ios_vs_android.csv'
NLP_OUTPUT_FILE = './nlp_result_combined.json'

DECODER = {
    0: 'Android',
    1: 'iPhone',
}

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
        user_name = row['user_name']
        if len(user_name.strip()) == 0:
            continue
        if user_name not in mp_data:
            # only add data if this user is not yet accounted for
            # Otherwise we should push this down the street
            mp_data[user_name] = {
                'c_preference': int(row['c_preference']),
            }

# load the intput - data from LIWC
with open(LIWC_OUTPUT_FILE, 'r') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for row in reader:
        user_name = filename_to_user_name(row['Filename'])
        liwc_data[user_name] = {}

        for liwc_key in LIWC_KEYS:
            liwc_data[user_name][liwc_key] = float(row[liwc_key])

with open(NLP_OUTPUT_FILE, 'r') as infile:
    nlp_data = json.load(infile)

TOTAL_TEST_COUNT = 1
TEST_SET_SIZE = 46

all_accu = []
all_pre = []
all_recall = []

test_headers = ['Test number', 'Correct', 'Incorrect', 'Percentage', 'Score' ]
test_table = []
# for test_count in range(TOTAL_TEST_COUNT):
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

    for user_name in mp_data.keys():
        # Output
        current_y = mp_data[user_name]['c_preference']

        # Input
        current_x = deepcopy(liwc_data[user_name].values())

        # Bias
        current_x.append(1)

        # NLP word count
        nlp_wc = nlp_data[user_name]['count']
        current_x.append(nlp_wc)

        for nlp_key in NLP_DATA_FIELD:
            nlp_count = nlp_data[user_name]['map'][nlp_key]
            # The value of this NLP feature
            current_x.append(nlp_count)

            # Percentage of this NLP feature
            percentage = 100.00 * float(nlp_count) / float(nlp_wc)
            current_x.append(percentage)

        if user_name not in TEST_SET:
            # X.append(liwc_data[user_name].values())
            X_train.append(current_x)
            y_train.append(current_y)
        else:
            # test_X.append(liwc_data[user_name].values())
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
        'rate': 0,  # Accuracy in term of percentage
        'score': 0, # Accuracy
        'recall': 0,
        'precision': 0,
        'table': None,
        'correct': 0,
        'incorrect': 0
    }

    # Header of the table we will print out
    headers = ['No', 'Username', 'WC', 'Preference']

    for layer0_count in range(20, 80):
        for layer1_count in range (20, 80):
            # for alfa_value in [1e-5, 2e-5, 3e-5, 1e-4, 2e-4, 3e-4]:
            for alfa_value in [1e-5]:
                clf = MLPClassifier(
                    solver='lbfgs',
                    alpha=alfa_value,
                    hidden_layer_sizes=(layer0_count, layer1_count),
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

                    # number of true positive - used to calculate precision and recall
                    'true_positive': 0,
                    'false_negative': 0
                }

                for i, user_name in enumerate(TEST_SET):
                    current_prediction = prediction[i]
                    current_test = y_test[i]
                    table_entry = [
                        i,
                        user_name,
                        liwc_data[user_name]['WC'],
                    ]
                    if current_prediction == current_test:
                        tally['correct'] += 1
                        colour = Fore.GREEN

                        if current_prediction == 1:
                            # This is true positive
                            tally['true_positive'] += 1
                    else:
                        tally['incorrect'] += 1
                        colour =  Fore.RED
                        if current_prediction == 0:
                            # This is false negative
                            tally['false_negative'] += 1
                    table_entry.append(colour + DECODER[current_prediction] + Style.RESET_ALL)
                    table.append(table_entry)

                # A very simple way to count the success rate
                success_rate = 100 * float(tally['correct']) / float(tally['correct'] + tally['incorrect'])

                test_score = clf.score(X_test, y_test)


                if optimal_score['score'] < test_score:
                    # A success
                    optimal_score = {
                        'layer0': layer0_count,
                        'layer1': layer1_count,
                        'alpha': alfa_value,
                        'rate': success_rate,
                        'score': test_score,
                        'table': deepcopy(table),
                        'correct': tally['correct'],
                        'incorrect': tally['incorrect'],
                        # Clculate the recall and precision for this network
                        'precision':  float(tally['true_positive']) / len([i for i in prediction if i == 0]),
                        'recall':  float(tally['true_positive']) / (tally['true_positive'] + tally['false_negative']),

                    }

    # if optimal_score['score'] < 0.73:
    #     continue
    print('Training Multilayer Neural Network with with {} training entries, each entry containing {} features'.format(
        len(X_train),
        len(X_train[0]),
    ))

    print('Optimal solution in term of score: \n NN with {} node in first hidden layers, {} hidden nodes in second one and alpha {}\n Correct/Incorrect: {}/{} ({}%, score: {})'.format(
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
    all_pre.append(optimal_score['precision'])
    all_recall.append(optimal_score['recall'])
    print('{} / {}'.format(
        Fore.YELLOW + str(test_count) + Style.RESET_ALL,
        Fore.BLUE + str(TOTAL_TEST_COUNT) + Style.RESET_ALL,
    ))
    # print (Fore.GREEN)
    # print(all_accu)
    # print(Style.RESET_ALL)

print('Overal result')
print tabulate(test_table, test_headers, tablefmt="plain")

print('Accuracies for all {} tests'.format(TOTAL_TEST_COUNT))
print(all_accu)
print('Recals on all all {} tests'.format(TOTAL_TEST_COUNT))
print(all_recall)
print('Precision on all all {} tests'.format(TOTAL_TEST_COUNT))
print(all_pre)
