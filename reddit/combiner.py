#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tagger.py
# A script that we use to tag speech parts for each user

import os, csv, random, string, json, sys, requests
from colorama import init, Fore, Back, Style
from common import *
from nltk import CoreNLPParser
init()

# Read out input file to get the list of users
input_data = []
user_data = {}

PREFERENCE_FILE = './ios_vs_android.csv'
NLP_DATA_DIR = './nlp_data'

# Market preference data - mapp from user to value
mp_data = {}

# Data from NLP - Map from user to values
nlp_data = {}

# List of username
user_names = []

with open(PREFERENCE_FILE, 'r') as infile:
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

## Read the NLP result file
for input_file in os.listdir(NLP_DATA_DIR):
    user_name = filename_to_user_name(input_file)
    user_names.append(user_name)
    with open ('{}/{}'.format(NLP_DATA_DIR, input_file), 'r') as in_file:
        temp_data = json.load(in_file)
        for nlp_key in NLP_DATA_FIELD:
            if nlp_key not in temp_data['map'].keys():
                # We did NOT find data for this field
                temp_data['map'][nlp_key] = 0
        nlp_data[user_name] = temp_data

with open(NLP_COMBINED_DATA, 'w') as out_file:
    json.dump(nlp_data, out_file)

