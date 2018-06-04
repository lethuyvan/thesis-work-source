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

INPUT_FILE = './ios_vs_android.csv'
INPUT_DIR = './crawled_data'
OUTPUT_DIR = './nlp_data'

NLP_URL = 'http://nlp:9000'

# Set up the parser beforehand
parser = CoreNLPParser(
    url=NLP_URL,
    encoding='utf8',
    tagtype='pos'
)

# Kind of lines we would like to ignore
IGNORE_LIST = [
    u'&nbsp;',
    u'**%100$ percent dollars**',
    u'Don’t waste your money. I spent $10 for this feature and only works %10 of the time, usually just breaks the page loading at all requiring whitelisting instead.',
    u'She’s using a 4S??? Get her the phone. %100',
    u'Edit: also worth to note, if you choose “don’t trust” when plugging in it will only charge at .5 because it doesn’t report itself as an iPhone, but that should still be way faster than %10 in three hours',
    u'It was horrendously buggy for me. I never had an issue with the actual function of sync seemed to keep my stuff in order between my iPad and iPhone, but man I could immeaditly tell when the sync started because my CPU would ramp up to %100 and my battery would start draining like crazy, and the messages app was so laggy I couldn’t even type, and would be like this for like 15+ minutes.',
    u'[I got the mandelbrot.](https://anvaka.github.io/pplay/?tx=0&ty=0&scale=1&fc=vec4%20get_color%28vec2%10p%29%20%7B%0A%20%20float%20t%20%3D%200.%3B%0A%20%20vec2%20z%20%3D%20p%3B%0A%20%20vec2%20c%20%3D%20vec2%280.60891%2C%200.89098%29%3B%0A%20%20float%20frames%20%3D%20600.%3B%0A%20%20float%20a%20%3D%203.14*%202.%20*%20bease%28mod%28iFrame%2C%20frames%29%2Fframes%29%3B%0A%0A%0A%20%20for%28int%20i%20%3D%200%3B%20i%20%3C%2032%3B%20%2B%2Bi%29%20%7B%0A%20%20%20%20if%20%28length%28z%29%20%3E%202.%29%20break%3B%0A%20%20%20%20z%20%3D%20c_mul%28c_exp%28z%29%20*%20sin%28a%29%2C%20z%29%20%2B%20c%3B%0A%20%20%20%20t%20%3D%20float%28i%29%3B%0A%20%20%7D%0A%0A%20%20return%20vec4%28length%28z%29%20*%20t%20*%20vec3%281.%2F64.%2C%201.%2F32.%2C%201.%2F16.%29%2C%201.0%29%3B%0A%7D)',
]


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
                line = line.decode('utf8')[:-1] # Remove trailing newline
                line_index += 1
                # Hacky
                if len(line.strip()) == 0:
                    # Blank line
                    continue
                if line.strip() in IGNORE_LIST:
                    # Skip this
                    continue
                print(u'[{}] [{}{:6d}{}] {}'.format(
                    Fore.CYAN + user_name + Style.RESET_ALL,
                    Fore.YELLOW, line_index, Style.RESET_ALL,
                    line
                ))
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
