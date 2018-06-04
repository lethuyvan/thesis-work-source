# -*- coding: utf-8 -*-
def user_name_to_filename(user_id):
    ''' Construct a file name from user_id
    '''
    return '{0}/{1}.txt'.format(
        OUTPUT_DIR,
        user_id
    )


def filename_to_user_name(filename):
    ''' Extract the user_id from filename
    '''
    return filename.split('.')[0].split('/')[-1]


LIWC_KEYS = [
    'WC',
    'money',
    'insight',
    # 'Filename', This is just filename, we ignore it for now
    'OtherP',
    'death',
    'informal',
    'ipron',
    'adj',
    'achieve',
    'bio',
    'risk',
    'leisure',
    'Dic',
    'verb',
    'they',
    'affect',
    'Parenth',
    'nonflu',
    'Authentic',
    'auxverb',
    'shehe',
    'SemiC',
    'pronoun',
    'Sixltr',
    'affiliation',
    'see',
    'home',
    'sexual',
    'space',
    'filler',
    'posemo',
    'netspeak',
    'health',
    'cause',
    'body',
    'we',
    'power',
    'focuspast',
    'article',
    'Apostro',
    'ingest',
    'motion',
    'swear',
    'social',
    'family',
    'feel',
    'number',
    'cogproc',
    'female',
'negate',
'negemo',
'differ',
'adverb',
'WPS',
'percept',
'Exclam',
'prep',
'friend',
'relig',
'hear',
'Tone',
'work',
'Period',
'focusfuture',
'male',
'function',
'compare',
'QMark',
'certain',
'assent',
'sad',
'Analytic',
'anger',
'conj',
'anx',
'ppron',
'Quote',
'focuspresent',
'quant',
'discrep',
'relativ',
'Colon',
'you',
'Segment',
'tentat',
'interrog',
'drives',
'AllPunc',
'i',
'Clout',
'Dash',
'Comma',
'time',
'reward'
]


# Test set - what we will use to test the model afterward
TEST_SET = [
    'TheElderCouncil',
    'stacecom',
    'nupogodi',
    'spoonyfork',
    'rreighe2',
    'kill-dash-nine',
    'mrstinkyfingers',
    'b_fnk',
    'K_Click_D',
    'o_Oz',
    'Biobak_',
    'Sozin91',
    'ScottRTL',
    'GENERALLY_CORRECT',
    'ForwardBias',
    'kickerofbottoms',
    'razorsoup',
    'JVO1317',
    'TheSaucerBoy',
    'RealShigeruMeeyamoto',
]

# Code for generating test set
# while len(TEST_SET) < 20:
#     # select a random user
#     val = None
#     while True:
#         val = random.choice(mp_data.keys())
#         if val not in TEST_SET:
#             break;
#     TEST_SET.append(val)


# print(TEST_SET)



# Data related to NLP
NLP_DATA_FIELD = [
    'CC', # Coordinating conjunction
    'CD', # Cardinal number
    'DT', # Determiner
    'EX', # Existential there
    'FW', # Foreign word
    'IN', # Preposition or subordinating conjunction
    'JJ', # Adjective
    'JJR', # Adjective, comparative
    'JJS', # Adjective, superlative
    'LS', # List item marker
    'MD', # Modal
    'NN', # Noun, singular or mass
    'NNS', # Noun, plural
    'NNP', # Proper noun, singular
    'NNPS', # Proper noun, plural
    'PDT', # Predeterminer
    'POS', # Possessive ending
    'PRP', # Personal pronoun
    'PRP$', # Possessive pronoun
    'RB', # Adverb
    'RBR', # Adverb, comparative
    'RBS', # Adverb, superlative
    'RP', # Particle
    'SYM', # Symbol
    'TO', # to
    'UH', # Interjection
    'VB', # Verb, base form
    'VBD', # Verb, past tense
    'VBG', # Verb, gerund or present participle
    'VBN', # Verb, past participle
    'VBP', # Verb, non­3rd person singular present
    'VBZ', # Verb, 3rd person singular present
    'WDT', # Wh­determiner
    'WP', # Wh­pronoun
    'WP$', # Possessive wh­pronoun
    'WRB', # Wh­adverb
]

NLP_COMBINED_DATA = 'nlp_result_combined.json'
