#!/usr/bin/env python

# simply_nn
# A basic NN to test our theory
# Document by http://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We use only one output from MP free data to try and train
# The feature come from LIWC

import os, csv, random, json, sys
from common import *
from tabulate import tabulate
from colorama import init, Fore, Back, Style
from copy import deepcopy
import numpy
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

user_ids = {
    'android': [],
    'iPhone': [],
}

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
            val = int(row['c_preference'])
            mp_data[user_name] = {
                'c_preference': val
            }
            if val == 0:
                user_ids['android'].append(user_name)
            else:
                user_ids['iPhone'].append(user_name)

# print(len(mp_data))

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

# Analyze the Android space
for os in ['android', 'iPhone']:
    print(os)
    wc = [nlp_data[user_name]['count'] for user_name in user_ids[os]]
    total_wc = sum(wc)
    user_count = len(user_ids[os])
    print('Users: {}\nReddit word count:\n  Total: {}\n  Mean: {}\n  Median: {}\n  Range: {} - {}\n'.format(
        user_count,
        total_wc,
        numpy.mean(wc),
        numpy.median(wc),
        numpy.min(wc), numpy.max(wc),
    ))
