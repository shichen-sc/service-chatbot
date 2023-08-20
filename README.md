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
    ´´´python
        key_words = ['hello', 'bye', 'satellite', 'tag', 'software', 'tracking']
    ´´´ 

- Synonyms
    - As these keywords can be addressed in different ways by different users, for example, hi, hello, or how are you. Thus, synonyms is being covered using method WordNet of module nltk. Which is a lexcial database for English language.
    - While the synonyms of those specific product name such as satellite, tag are being maintained manually. As normall these alternative words are quite familiar and standardized in industrial area. For example, some customers may use anchor instead of satellite.
    ´´´python
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
    ´´´

- The Header
    - The header shows the most important feature of the learning platform that "driven by the AI"
    - The header tells the users that the platform aims to provide a flexible and customized learning experience using the AI technology
    - The header provides a link for the users to select the disired language, level (same as the Start Learning in the navigiation, which is currently not implemented yet)
    - The headers contains a image that clearly shows it is language learning platform
    ![A screenshot of the header](/assets/images/README/header.png)

- The Feature Section
    - The feature section lists 4 main features that makes the platform special:
        - AI-driven conversation, which tells the users that the platform uses heavily AI technology to provide the users conversation with all scenarios
        - Up-to-date news, which tells the users that the platform provides update-to-date-news written in a level that fits to the user, instead of providing the traditional text books
        - Learning group, which tells the users that the users can create or join a learning group on the platform directly
        - Talk to native speakers, which tells the users that the platform provides a lot of qualified native speakers
    ![A screenshot of the feature section](/assets/images/README/feature.png)

- The Video Section
    - The video section contains a youtube video, that explains the user how AI can enhance the language learning experience. (The video should be ultimately created by Learn Through, apparently there is no such a material yet, and therefore, a relevant youtube video is being used.)
    ![A screenshot of the video section](/assets/images/README/video.png)

- The Comment Section
    - The comment section allows the users to review some of the comments from the students who have already registered and used the platform. So that the users know better how Learn Through can help and what is special at Learn Through
    ![A screenshot of the comment section](/assets/images/README/comment.png)

- The Footer
    - The footer contains again the logo of the platform
    - The footer contains again a clickable anchor that directs the user to the next page where they should select the desired language and level (currently not implemented yet)
    - The footer contains the social media links of the platform, facebook, twitter, youtube, instagram. (As of there is no official link yet, the landing page of each is being used)
    ![A screenshot of the footer](/assets/images/README/footer.png)

## Testing

- I tested and confirmed that the page works in browsers: Chrome, Firefox
- I confirm that this project is responsive

## Bugs

### Solved bugs
- When the screen width is smaller as 950px, the anchor element in the header is not clickable
    - The issue is that the hero image overlaps with the anchor. To solve, z-index: 1 is being added to the style for this anchor element
    ```
    #hero-text {
        top: 20%;
        left: 50%;
        transform: translate(-50%, -20%);
        clear: left;
        z-index: 1;
    }
    ```

### Unsolved bugs
- As the navigation bar is being fixed on the top of the page, once i click on the next slide in the comment section, the view of the page will be reset to middle, as a result, part of the photo of the students are being hidden by the navigation bar, see the picture here
![A screenshot of the bug](/assets/images/README/bug.png)

## Validator Testing

- HTML
    - No erros were returned when passing through the official W3C validator
- CSS
    - No errors were found when passing through the official (Jigsaw) validator
- Accessibility
    - I confirmed that the colors and fonts chosen are easy to read and accessible by running it through lighthouse in devtools
    ![A screenshot of the scores estimated by lighthouse](/assets/images/README/lighthouse.png)

## Deployment

- The site was deployed to Github pages. The steps to deploy are as follows:
    - In the GitHub repository, navigate to the Settings tab
    - Click on Page from the side menu
    - Choose main for the Branch, and click on save
    - Wait and refresh the page, the link to the page should be generated
- Link for the page:
    - [Learn Through](https://shichen-sc.github.io/learn-through/)


## Credits

### Content
- The code to make the social media links was taken from the CI [Love Running](https://github.com/shichen-sc/love-running) Project
- The code for the comment section was referenced from [Codepen](https://codepen.io/Schepp/pen/WNbQByE)

### Media
- The images in the project were all take from [Freepik](https://www.freepik.com/free-photos-vectors)

## To-Do
- Solve the open bug (described above)
- Write html as the link for the button "Start Learning" on the navigation bar, where the users can select the desired language and current level
- Write html for Sign Up and Login