# -*- coding: utf-8 -*-
OUTPUT_DIR = './agregated'
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
# TEST_SET = [
#     '666c166767bb6645ee3dde9804faa6a9',
#     '1d6d222bd3fb4c0af35466042cb82d78',
#     'ab38affacd75668b8eaf1df27e8b5be8',
#     'da56abb46f342d8e4b4bc96165cd645d',
#     '96487b200f227f3f845bb8851dad2139',
#     'e2cc76f16ed40953e5c082ff5ef9a2e9',
#     '9f320ade181aa12bf10361871afa8d90',
#     'e4a9de8d77c21c3f704fdb0055cdde43',
#     '2ea1efd66ffc011621a4a74e06005e23',
#     'ed1dbabbe3ea7fd3f44efc6f6a96db68',
#     'c255a1cb2939ce6b4719a8a0cc085624',
#     '83b6e605652dbf6915856eea1ce419bd',
#     'b05f34be807a91ce0325cda601bc5856',
#     '80a570b74f23f56c94f639436ff92353',
#     'a1c187cbf8532b649cc3b36c01a3ca20',
#     'e0576e496b3bc5bd1046315ddb72646a',
#     '142635bd7f9ed8e4d8c292fa6ccd9aa4',
#     '709606429cd1b0d5cefaf63cdeaaa86b',
#     'e557fd2902b857797cb8cec471f201a5',
#     'fe22087986fdcc65939c793fe0ec90a9',
#     'eac7f51d95da0fefde6ecc692dcf85cc',
#     'd2ee2871aa02698e66fdc72b2218cdd8',
#     'b84d2613c4cf4e73f9c230f57facf66c',
#     'cf5a3f66c42918587a1428a6f7d7eec9'
# ]

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
    'WDT', # W-­determiner
    'WP', # Wh-pronoun
    'WP$', # Possessive wh-pronoun
    'WRB', # Wh-adverb
]

NLP_COMBINED_DATA = 'nlp_result_combined.json'
