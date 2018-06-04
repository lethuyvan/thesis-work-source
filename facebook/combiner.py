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

NLP_DATA_DIR = './nlp_data'

# Data from NLP - Map from user to values
nlp_data = {}

# List of username
user_names = []

## Read the NLP result file
for input_file in os.listdir(NLP_DATA_DIR):
    user_name = filename_to_user_id(input_file)
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

