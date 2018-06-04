#!/usr/bin/env python

# agregator.py
# Combine all the FB statuses to one file per user

import os, csv, io
from common import *

INPUT_FILE = 'mypersonality_final.csv'
OUTPUT_DIR = './agregated'

# Cleaup the dir before hand
folder = '/path/to/folder'
for the_file in os.listdir(OUTPUT_DIR):
    file_path = os.path.join(OUTPUT_DIR, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception as e:
        print(e)

constructed_data = {}


with open(INPUT_FILE, mode='r') as infile:
    reader = csv.DictReader(infile)

    # Read and construct data
    for row in reader:
        user_id = row['#AUTHID']
        status = row['STATUS'].lower()
        if user_id not in constructed_data:
            constructed_data[user_id] = []
        constructed_data[user_id].append(status)

for user_id in constructed_data:
    user_statuses = constructed_data[user_id]
    file_name = user_id_to_filename(user_id)
    print('Print out all statuses of {0} to {1}'.format(
        user_id,
        file_name
    ))
    with open(file_name, 'w') as outfile:
        outfile.write('\n'.join(user_statuses))
