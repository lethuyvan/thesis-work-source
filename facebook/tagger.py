#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tagger.py
# A script that we use to tag speech parts for each user

import os, csv, random, string, json, sys, requests
from colorama import init, Fore, Back, Style
from nltk import CoreNLPParser
init()

# Read out input file to get the list of users
input_data = []
user_data = {}

INPUT_FILE = './mypersonality_final.csv'
INPUT_DIR = './agregated'
OUTPUT_DIR = './nlp_data'

NLP_URL = 'http://nlp:9000'

# Set up the parser beforehand
parser = CoreNLPParser(
    url=NLP_URL,
    encoding='utf8',
    tagtype='pos'
)

# Kind of lines we would like to ignore
IGNORE_LIST = []


def user_id_to_input_filename(user_id):
    ''' Construct a file name from user_id
    '''
    return '{0}/{1}.txt'.format(
        INPUT_DIR,
        user_id
    )

def user_id_to_output_filename(user_id):
    ''' Construct a file name from user_id
    '''
    return '{0}/{1}.json'.format(
        OUTPUT_DIR,
        user_id
    )


## Read the input data
# with open(INPUT_FILE, mode='r') as infile:
#     reader = csv.DictReader(infile)

#     # Read and construct data
#     for row in reader:
#         user_url = row['user_url']
#         user_name = user_url.split('/')[-1]
#         row['user_name'] = user_name
#         input_data.append(row)
all_users = []
with open(INPUT_FILE, mode='r') as infile:
    reader = csv.DictReader(infile)

    # Read and construct data
    for row in reader:
        user_id = row['#AUTHID']
        if user_id not in all_users:
            all_users.append(user_id)
            input_data.append({
                'user_name': user_id,
            })

# Crawl the users
for data_entry in input_data:
    user_name = data_entry['user_name']

    if len(user_name) == 0:
        # Ending point
        print('No more users to process')
        break;

    input_file = user_id_to_input_filename(user_name)
    output_file = user_id_to_output_filename(user_name)
    # Check if we already have the output for this user, if yes - Just skip this user
    if os.path.isfile(output_file):
        # This file already exist
        print(Fore.GREEN +'  Skip' + Style.RESET_ALL)
        continue;
    else:
        # We haven't crawled this user yet - do it now
        print('Apply POS tag onto texts of user ' + Fore.GREEN + user_name + Style.RESET_ALL)

        # A frequency map
        user_data[user_name] = {
            'map': {},
            'count': 0,
        }

        with open(input_file, 'r') as in_file:
            line_index = 0
            for line in in_file:
                # line = line.decode('utf8')[:-1] # Remove trailing newline
                line = line[:-1] # Remove trailing newline
                line_index += 1
                # Hacky
                if len(line.strip()) == 0:
                    # Blank line
                    continue
                if line.strip() in IGNORE_LIST:
                    # Skip this
                    continue
                try:
                    print(u'[{}] [{}{:6d}{}] {}'.format(
                        Fore.CYAN + user_name + Style.RESET_ALL,
                        Fore.YELLOW, line_index, Style.RESET_ALL,
                        line
                    ))
                except UnicodeDecodeError:
                    print('  Cannot print')
                    continue
                try:
                    text_tokens = list(parser.tokenize(line))
                    tag_result = parser.tag(text_tokens)
                    # print(tag_result)
                    for tag_obj in tag_result:
                        tag_text = tag_obj[0]
                        tag_name = tag_obj[1]

                        # Save such result
                        user_data[user_name]['count'] += 1
                        if tag_name not in user_data[user_name]['map']:
                            user_data[user_name]['map'][tag_name] = 0
                        user_data[user_name]['map'][tag_name] += 1
                except ValueError:
                    print(Fore.RED + ' Failed - Value Error' + Style.RESET_ALL)
                    continue
                except requests.exceptions.HTTPError:
                    print(Fore.RED + ' Failed - HTTP Error' + Style.RESET_ALL)
                    continue
                except KeyboardInterrupt:
                    print('Exit')
                    sys.exit(2)
                except:
                    print(Fore.RED + ' Failed - Generic Error' + Style.RESET_ALL)
                    continue

        with open(output_file, 'w') as out_file:
            json.dump(user_data[user_name], out_file)
    print(Fore.GREEN +'  DONE' + Style.RESET_ALL)

print(user_data)
