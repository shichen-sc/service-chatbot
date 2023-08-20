import nltk
from nltk.corpus import wordnet

# global variables
# key words as key for the user input
key_words = ['hello', 'bye', 'satellite', 'tag', 'software', 'tracking']
# intent list as the intent of the user input
key_list = ['greeting', 'ending', 'sat_related', 'tag_related', 'sw_related', 'track_related']
#responses as the response content of the chat bot
responses = {
    'default_block': 'Hello! I am the Service Chatbot from XXX Technologies GmbH. \
            I am happy to provide you the 2nd level service support. \
            How can I help you?\n',
    'greeting': "Hi, please describe your issue. For example, one tag can't be tracked anymore. \
            If you want to quit, type in Bye or ctrl + c.\n",
    'ending': 'Goodbye! I wish you further success with our products.\n',
    'sat_related' : 'satellite_content\n',
    'tag_related': 'tag_content\n',
    'sw_related': 'software_content\n',
    'track_related': 'tracking_content\n',
    'other_topic': 'other_content\n'
}

# generate dictionary containing synonyms of the key words, as different users may use different wording for same question
def generate_synonyms_dict(key_words):
    dict_synonyms = {}

    for word in key_words:
        synonyms = []
        if word == 'hello':
            for each_syn in wordnet.synsets(word):
                for each_lem in each_syn.lemmas():
                    synonyms.append(each_lem.name())
            dict_synonyms[word] = set(synonyms)

        elif word == 'bye':
            for each_syn in wordnet.synsets(word):
                for each_lem in each_syn.lemmas():
                    synonyms.append(each_lem.name())
            #as quit and exit can also used by user to end conversation session instead of lemmatisation of Bye
            synonyms.extend(['quit', 'exit'])
            dict_synonyms[word] = set(synonyms)
        # the following words are the names of the product, thus manually extend the similar wording
        elif word == 'satellite':
            synonyms.extend(['satellite', 'anchor'])
            dict_synonyms[word] = set(synonyms)
        elif word == 'tag':
            synonyms.extend(['tag', 'badge'])
            dict_synonyms[word] = set(synonyms)
        elif word == 'software':
            synonyms.extend(['UI', 'ui', 'user interface', 'operating interface'])
            dict_synonyms[word] = set(synonyms)
        elif word == 'tracking':
            synonyms.extend(['tracking', 'tracking quality', 'tracking performance', 'tracking accuracy'])
            dict_synonyms[word] = set(synonyms)
    
    #print(dict_synonyms)
    return dict_synonyms