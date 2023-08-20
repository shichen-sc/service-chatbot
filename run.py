import nltk
from nltk.corpus import wordnet
import re
from datetime import datetime
from rich.console import Console
import sys

# global variables
# key words as key for the user input
key_words = ['hello', 'bye', 'satellite', 'tag', 'software', 'tracking']
# intent list as the intent of the user input
key_list = ['greeting', 'ending', 'sat_related', 'tag_related', 'sw_related', 'track_related']
#responses as the response content of the chat bot
responses = {
    'default_block' : 'Hello! I am the Service Robot from XXX Technologies GmbH. I am happy to provide you the 2nd level service support. How can I help you?\n', 
    'greeting': "Hi, please describe your issue. For example, one tag can't be tracked anymore. If you want to quit, type in Bye or press ctrl + c.\n",
    'ending': 'Goodbye! I wish you further success with our products.\n',
    'sat_related' : 'Regarding to satellites, we have the following suggestions: \n' + 
            '    1. Check the LED of the satellite, when everything is normal, you should see [bold]white[/] color. \n' +
            '    2. If you see [bold blue]blue[/], it means the satellite is not being detected via network, try to restart it by unplugging and plugging the ethernet cable. \n' +
            '    3. If you see [bold red]red[/], it means the satellite has a fatal [bold red]error[/], try to restart it by unplugging and plugging the ethernet cable. \n' +
            '    If you still have the error behavior, you probably have a defective hardware. Please contact [bold]3rd_level_support@xxx.com[/].',
    'tag_related': 'Regarding to tags, we have the following suggestions: \n' + 
            '    1. Make sure they are fully charged, you should see the led blinking [bold yellow]0.5Hz yellow[/] when they are being charged correctly. \n' +
            '    2. If they are being tracked by the system, you should see the led blinking [bold green]1Hz green[/] if you shake them. \n' +
            '    3. If the tag has battery and not working normally, try to do a reset cycle by pressing the button on the tag for [bold]10 seconds[/] until it blinks [bold red]red[/]\n' +
            '    If you still have the error behavior, you probably have a defective hardware. Please contact [bold]3rd_level_support@xxx.com[/].',
    'sw_related': 'Regarding to the software issue, we have the following suggestions: \n' +
            '    1. Make sure you have the newest release version [bold]2023.02[/], if not, please update it by pulling the image from our repository \n' +
            '    2. If you have problem to access the ui, please check your network and make sure you are in the same subnet as our server. Sometimes a reboot of the server may help. \n' +
            '    If you still have the error behavior, please contact [bold]3rd_level_support@xxx.com[/].',
    'track_related': 'Regarding to the tracking issue, we have the following suggestions: \n' +
            '    1. Check the LEDs of the satellites, they have to be [bold white]white[/]. \n' +
            '    2. If you have overally abnormal status of satellites, make sure the satellites are in the same network subnet as the server and try to reboot the system. \n' +
            '    3. If you have a poor accuracy in one specific area, you should confirm if you have possible interferences such as 5G communication or big metal construction. \n' +
            '    If you still have the error behavior, please contact [bold]3rd_level_support@xxx.com[/].',
    'other_topic': "Sorry, i don't get you. Try to describe your question more specifically. Or try to contact our 3rd level support via [bold]3rd_level_support@xxx.com[/]."
#file to record the user's input
filename = './session.txt'

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

# generate dictionary containing keywords to identify intent of the question.
def generate_keywords_dict(list_words, key_list):
    dict_synonyms = generate_synonyms_dict(list_words)
    
    keywords = {key:[] for key in key_list}
    keywords['greeting'] = []
    for each in list(dict_synonyms['hello']):
        keywords['greeting'].append('.*' + each + '.*')

    keywords['ending'] = []
    for each in list(dict_synonyms['bye']):
        keywords['ending'].append('.*' + each + '.*')

    for each in list(dict_synonyms['satellite']):
        keywords['sat_related'].append('.*' + each + '.*')
        keywords['sat_related'].append('.*' + each + '.*' + "n't" + '.*')
        keywords['sat_related'].append('.*' + each + '.*' + 'not' + '.*')
        keywords['sat_related'].append('.*' + each + '.*' + 'issue' + '.*')
        keywords['sat_related'].append('.*' + each + '.*' + 'problem' + '.*')
        keywords['sat_related'].append('.*' + 'issue' + '.*' + each + '.*')
        keywords['sat_related'].append('.*' + 'problem' + '.*' + each + '.*')

    for each in list(dict_synonyms['tag']):
        keywords['tag_related'].append('.*' + each + '.*' + "n't" + '.*')
        keywords['tag_related'].append('.*' + each + '.*' + 'not' + '.*')
        keywords['tag_related'].append('.*' + each + '.*' + 'issue' + '.*')
        keywords['tag_related'].append('.*' + each + '.*' + 'problem' + '.*')
        keywords['tag_related'].append('.*' + 'issue' + '.*' + each + '.*')
        keywords['tag_related'].append('.*' + 'problem' + '.*' + each + '.*')
        keywords['tag_related'].append('.*' + each + '.*' + 'tracked' + '.*')
        keywords['tag_related'].append('.*' + each + '.*' + 'accuracy' + '.*')


    for each in list(dict_synonyms['software']):
        keywords['sw_related'].append('.*' + each + '.*' + "n't" + '.*')
        keywords['sw_related'].append('.*' + each + '.*' + 'not' + '.*')
        keywords['sw_related'].append('.*' + each + '.*' + 'issue' + '.*')
        keywords['sw_related'].append('.*' + each + '.*' + 'problem' + '.*')
        keywords['sw_related'].append('.*' + each + '.*' + 'accessed' + '.*')
        keywords['sw_related'].append('.*' + 'issue' + '.*' + each + '.*')
        keywords['sw_related'].append('.*' + 'problem' + '.*' + each + '.*')
        keywords['sw_related'].append('.*' + 'access' + '.*' + each + '.*')


    for each in list(dict_synonyms['tracking']):
        keywords['track_related'].append('.*' + each + '.*' + "n't" + '.*')
        keywords['track_related'].append('.*' + each + '.*' + 'not' + '.*')
        keywords['track_related'].append('.*' + each + '.*' + 'issue' + '.*')
        keywords['track_related'].append('.*' + each + '.*' + 'problem' + '.*')
        keywords['track_related'].append('.*' + each + '.*' + 'bad' + '.*')
        keywords['track_related'].append('.*' + 'bad' + '.*' + each + '.*')
        keywords['track_related'].append('.*' + 'issue' + '.*' + each + '.*')
        keywords['track_related'].append('.*' + 'problem' + '.*' + each + '.*')

    #print(generate_keywords_dict(list_words, key_list))
    return keywords

# using regular expression to compile pattern for each keyword
def create_patterns(list_words, key_list):
    keywords = generate_keywords_dict(list_words, key_list)
    patterns = {}

    for intent, keys in keywords.items():
        patterns[intent] = re.compile('|'.join(keys))

    #print(patterns)
    return patterns

# function to match intent
def match_intent(message):
    matched_intent = None
    
    for intent,pattern in patterns.items():
        if re.search(pattern, message):
            matched_intent=intent

    return matched_intent

# function to give response
def respond(message):
    intent=match_intent(message)
    
    key='other_topic'
    
    if intent in responses:
        key=intent
    
    return responses[key]

# function to send user input
def send_message(message):
    return respond(message)

# check the session number and write session number for current conversation
def check_session_number():
    count = 1
    with open(filename, 'r+') as file:
        lines = file.readlines()
        for line in lines:
            if 'SESSION' in line:
                count += 1
        file.write(f'\nSESSION {count}:\n')

# record the user input and save it into a txt file
def record_message(message):
    timestamp = datetime.now().strftime('%Y-%D %H:%M:%S')
    with open(filename, 'a') as file:
        file.write(f'{timestamp}: {message}\n')

def main():
    global patterns 
    patterns = create_patterns(list_words, key_list)
    #print(patterns)
    check_session_number()
    console = Console()
    console.print('[bold magenta]Service Bot: [/]' + responses['default_block'])
    flag = True
    while(flag==True):
        console.print('[bold magenta]You: [/]', end = '')
        user_input = input().lower()
        record_message(user_input)
        #console.print(user_input)
        matched_intent = match_intent(user_input)

        if matched_intent == 'ending':
            flag = False
            console.print('[bold magenta]Service Bot: [/]' + responses['ending'])
        else:
            response = send_message(user_input)
            console.print('[bold magenta]Service Bot: [/]' + response)

if __name__ = '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted by User...')
        sys.exit(0)