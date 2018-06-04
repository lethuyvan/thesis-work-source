#!/usr/bin/env python

# simply_nn
# A basic NN to test our theory
# Document by http://scikit-learn.org/stable/modules/neural_networks_supervised.html
# We use only one output from MP free data to try and train
# The feature come from LIWC

import matplotlib
matplotlib.use('Agg')
from os import path
import os, csv, random, json, sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt

FREE_DATA_FILE = './ios_vs_android.csv'
NLP_OUTPUT_FILE = './nlp_result_combined.json'

user_ids = {
    'android': [],
    'iPhone': [],
}

# Mapping from user ID to their output values
mp_data = {}

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

# Read the whole text.

# Display the generated image:
# the matplotlib way:
for os in [
    # 'android',
    'iPhone'
]:
    print(os)
    text = ''
    file_counter = 0
    for user_name in user_ids[os]:
        text += open('./crawled_data/{}.txt'.format(user_name), 'r').read()
        file_counter += 1
        # break
    print('{} files'.format(file_counter))
    # Generate a word cloud image
    wordcloud = WordCloud(max_words=1000,
                          margin=10,
                          random_state=1,
                          max_font_size = 40,
                          ).generate(text)

    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure(figsize=(10,4))
    file_name = '1000_most_word_cloud_{}.png'.format(os)
    # wordcloud.to_file(file_name)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()

    # lower max_font_size
    # wordcloud = WordCloud(max_font_size=40).generate(text)
