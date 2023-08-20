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