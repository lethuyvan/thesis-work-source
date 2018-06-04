#!/usr/bin/env python

# simply_nn
# A basic NN to test our theory
# Document by http://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We use only one output from MP free data to try and train
# The feature come from LIWC

import os, csv, random
from colorama import init, Fore, Back, Style
init()

# Reddit part
import praw

# Create the reddit client
reddit = praw.Reddit(client_id='P4sgWL4oUIItTA',
                     client_secret='HpgLbZ5c0aDmCXEtT4zAgpKUa_I',
                     user_agent='simple-search')

# Read out input file to get the list of users
input_data = []
user_data = {}

INPUT_FILE = './ios_vs_android.csv'
OUTPUT_DIR = './crawled_data'
USER_POST_LIMIT = 10000

def user_id_to_filename(user_id):
    ''' Construct a file name from user_id
    '''
    return '{0}/{1}.txt'.format(
        OUTPUT_DIR,
        user_id
    )


def filename_to_user_id(filename):
    ''' Extract the user_id from filename
    '''
    return filename.split('.')[0].split('/')[-1]

## Read the input data
with open(INPUT_FILE, mode='r') as infile:
    reader = csv.DictReader(infile)

    # Read and construct data
    for row in reader:
        user_url = row['user_url']
        user_name = user_url.split('/')[-1]
        row['user_name'] = user_name
        input_data.append(row)

# Crawl the users
for data_entry in input_data:
    user_name = data_entry['user_name']
    output_file = user_id_to_filename(user_name)

    if len(user_name) == 0:
        # Ending point
        print('No more users to crawl')
        break;

    # Check if we already have the output for this user, if yes - Just skip this user
    if os.path.isfile(output_file):
        # This file already exist
        continue;
    else:
        # We haven't crawled this user yet - do it now
        print('Crawling last {} comments from user '.format(USER_POST_LIMIT) + Fore.GREEN + user_name + Style.RESET_ALL)
        r_user = reddit.redditor(user_name)
        latest_comments = r_user.comments.new(limit=USER_POST_LIMIT)
        comment_array = [ comment.body for comment in latest_comments ]
        user_data[user_name] = comment_array
        print('  Write all comments from this user into ' + Fore.BLUE + output_file + Style.RESET_ALL)
        with open(output_file, 'w') as outfile:
            outfile.write('\n'.join(comment_array).encode('utf8'))
        print(Fore.GREEN +'  DONE' + Style.RESET_ALL)

    # break;



# Check the users
# user = reddit.redditor('tigno')
# for comment in user.comments.new(limit=10):
#     print comment.body
