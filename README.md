# Service Chatbot

Nowadays more and more companies are making use of chat bots to interact with the uses as first contact in the business process, in order to be able to deliver answers faster to the users.

A chat bot does have a few advantages, fast to respond, give customers first-hand guiding information, the conversation data can be used for further purpose for better analysis.

There are mainly two ways of a conversational chat bot: 
- Rule Based chatbot
- Self Learning chatbot

The approach to this project is a rule based chat bot:
- The bot answers query based on certain rules being defined.
- It is good at providing necessary information for an industrial product customers, with which customer is able to check their problems before they reach out to the 3rd level support.

## Features

- Keywords
    - Keywords in an product error case can be normally eaily defined, for example, in this project, it is the hardware satellite, tag, tracking, software. Including the normal greeting words, such as hi, hello, goodbye. Alle these keywords are defined as a global variable:
    ```
        key_words = ['hello', 'bye', 'satellite', 'tag', 'software', 'tracking']
    ``` 

- Synonyms
    - As these keywords can be addressed in different ways by different users, for example, hi, hello, or how are you. Thus, synonyms is being covered using method WordNet of module nltk. Which is a lexcial database for English language.
    - While the synonyms of those specific product name such as satellite, tag are being maintained manually. As normall these alternative words are quite familiar and standardized in industrial area. For example, some customers may use anchor instead of satellite.
    ```
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
    ```

- Intent of User Input
    - Regular expression is being used here in order to identify intent of the question (user input). For example, user can greet by typing "hi", "hello", etc. And all these will be treated as a value of the intent key "greeting".
    - Same is applied for the other intent, for example, intent "sat_related" includes "I have a problem on one satellite", "one of the satellites are not lighting up."
    ```
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
    ```

- Compile
    - These intent patterns will be further compiled into regular expression object using re.compile().
    ```
    def create_patterns(key_words, key_list):
    keywords = generate_keywords_dict(key_words, key_list)
    patterns = {}

    for intent, keys in keywords.items():
        patterns[intent] = re.compile('|'.join(keys))

    #print(patterns)
    return patterns
    ```

- Responses
    - Responses of the chat bot are maintained in a dictionary:
    ```
    responses = {
    'default_block' : 'Hello! I am the Service Robot from XXX Technologies GmbH. I am happy to provide you the 2nd level service support. How can I help you?', 
    'greeting': "Hi, please describe your issue. For example, one tag can't be tracked anymore. If you want to quit, type in Bye or press ctrl + c.",
    'ending': 'Goodbye! I wish you further success with our products.',
    'sat_related' : 'Regarding to satellites, we have the following suggestions: \n' + 
            '    1. Check the LED of the satellite, when everything is normal, you should see [bold]white[/] color. \n' +
            '    2. If you see [bold blue]blue[/], it means the satellite is not being detected via network, try to restart it by unplugging and plugging the ethernet cable. \n' +
            '    3. If you see [bold red]red[/], it means the satellite has a fatal [bold red]error[/], try to restart it by unplugging and plugging the ethernet cable. \n' +
            '    If you still have the error behavior, you probably have a defective hardware. Please contact [bold]3rd_level_support@xxx.com[/].',
    ```
    - And the user input will be checked to find the intent, and then passed further to get a proper answer:
    ```
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
    ```

- Recording User's Input
    - For each session of conversation, the user input will be written in to a session.txt file. The file will be checked for the number of session, then will be initiated with a correction session number, e.g. SESSION 2, afterwards, each user input will be recorded with a timestamp.
    ```
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
    ```
    
- Rich Console
    - In order to make the terminal more readable, method Console from module rich is being used. This allows to apply some style to some wording, for example, bold, color.
    ```
    console = Console()
    console.print('[bold magenta]Service Bot: [/]' + responses['default_block'])
    ```

- Start Chat Bot
    - Bot will be started with initializing the session.txt file and a welcome response "default_block"
    - A variable flag is being set in order to control the terminal loop
    - User can type 'bye', 'quit', 'exit' or ctrl+c to stop the terminal
    - And the session.txt will be printed out onto the terminal after the termination only to prove the content exists (this can be removed of course)
    ```
    def main():
    global patterns 
    patterns = create_patterns(key_words, key_list)
    #print(patterns)
    check_session_number()
    console = Console()
    console.print('[bold magenta]Service Bot: [/]' + responses['default_block'])
    flag = True
    while(flag==True):
        console.print('[bold magenta]You: [/]', end = '')
        user_input = input('\n').lower()
        record_message(user_input)
        #console.print(user_input)
        matched_intent = match_intent(user_input)

        if matched_intent == 'ending':
            flag = False
            console.print('[bold magenta]Service Bot: [/]' + responses['ending'])
        else:
            response = send_message(user_input)
            console.print('[bold magenta]Service Bot: [/]' + response)

    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            print('\nInterrupted by User...')
            show_session_record()
            sys.exit(0)
    ```

## Testing
    ```
    [nltk_data]   Package wordnet is already up-to-date!
    Service Bot: Hello! I am the Service Robot from XXX Technologies GmbH. I am happy to provide 
    you the 2nd level service support. How can I help you?
    You: 
    I can't charge the tags..
    Service Bot: Regarding to tags, we have the following suggestions: 
        1. Make sure they are fully charged, you should see the led blinking 0.5Hz yellow when they
    are being charged correctly. 
        2. If they are being tracked by the system, you should see the led blinking 1Hz green if 
    you shake them. 
        3. If the tag has battery and not working normally, try to do a reset cycle by pressing the
    button on the tag for 10 seconds until it blinks red
        If you still have the error behavior, you probably have a defective hardware. Please 
    contact 3rd_level_support@xxx.com.
    You: 
    ^C
    Interrupted by User...
    Following is the record of user input of each session: 

    SESSION 1:
    2023-08/20/23 22:07:33: hi
    2023-08/20/23 22:07:59: i have a problem on one of the satellites.
    2023-08/20/23 22:09:46: how about tag?
    2023-08/20/23 22:09:56: i have a issue on tag

    SESSION 2:
    2023-08/20/23 23:53:53: hi
    2023-08/20/23 23:54:06: i can't charge the tags.

    SESSION 3:
    2023-08/20/23 23:55:47: i can't charge the tags.
    ```

## Deployment

- 

