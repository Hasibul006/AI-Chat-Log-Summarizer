#importing all the necessary libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import string

#extracting messages of user and ai separately
def parsing_Messages(file_path):
    users_message = []
    ai_messages = []

    #reading the file line by line
    with open(file_path, 'r') as chats:
        for line in chats:
            if line.startswith('User: '):
                users_message.append(line[6:].strip())
            elif line.startswith('AI: '):
                ai_messages.append(line[4:].strip())

    return users_message, ai_messages


#removing stopwords and punctuations from the text
def avoiding_stopwords_punctuations(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            #isalpha() checks if the token is a word
            filtered_tokens.append(token)

    return filtered_tokens


#getting the top keywords calculating the tfidf
def get_top_keywords(messages, top_n=5):

    #creating a vectorizer for the messages to calculate tfidf
    vectorizer = TfidfVectorizer(
        tokenizer=avoiding_stopwords_punctuations,
        lowercase=True
    )

    tfidf_matrix = vectorizer.fit_transform(messages) #learning the keywords and converts the messages into vectors(tfidf)
    feature_names = vectorizer.get_feature_names_out() #gets the list of keywords
    scores = tfidf_matrix.sum(axis=0).A1 #sums the tfidf values of each keyword accross all the messages
    word_scores = dict(zip(feature_names, scores)) #combines the words with their scores
    top_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True) #sorts the keywords based on their scores
    
    return top_keywords[:top_n]


# getting the common words using nltk
def get_common_words(messages, top_n=5):
    stop_words = set(stopwords.words('english')) #getting the stop words
    words = []

    #tokenizing the messages avoiding the stop words and punctuations
    for msg in messages:
        tokens = word_tokenize(msg.lower())
        for word in tokens:
            if word.isalpha() and word not in stop_words: #isalpha() checks if the token is a word
                words.append(word)

    word_counts = Counter(words) #counts the frequency of each word
    return word_counts.most_common(top_n)


#function for generating the summary of a single file
def generate_summary(filepath):

    #if the file does not exist
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return
    
    #calling function for getting the messages
    users_message, ai_messages = parsing_Messages(filepath)

    #calculating the number of messages
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages

    #calling the function for getting the top keywords
    common_words = get_top_keywords(users_message + ai_messages)
    #common_words = get_common_words(users_message + ai_messages)

    # considering the top 3 keywords as main topics of the conversation
    topics = [word for word, _ in common_words[:3]]

    #decorating the summary
    summary = f"""Summary of a single file:
    - The conversation had {num_total_messages} exchanges.
    - The user asked mainly about {', '.join(topics[:2])}.
    - Most common keywords: {', '.join(topics)}.
    """

    #writing the summary to a file
    with open('summarySingleFile.txt', 'w') as summary_file:
        summary_file.write(summary)
    print(summary)


#function for generating the summary of multiple files
def generate_summary_form_multiple_files(folder_path):

    users_message = []
    ai_messages = []

    #if the folder does not exist
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found.")
        return
    
    #iterating over all the files with extension .txt in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            users, ai = parsing_Messages(filepath) #calling the function for getting the messages
            users_message.extend(users)
            ai_messages.extend(ai)
    
    #calculating the number of messages
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages

    #calling the function for getting the top keywords using tfidf
    common_words = get_top_keywords(users_message + ai_messages)

    # considering the top 3 keywords as main topics of the conversation
    topics = [word for word, _ in common_words[:3]]

    #decorating the summary
    summary = f"""This the summary of multiple files:
    - The conversation had {num_total_messages} exchanges.
    - The user asked mainly about {', '.join(topics[:2])}.
    - Most common keywords: {', '.join(topics)}.
    """

    #writing the summary to a file
    with open('summaryMultipleFiles.txt', 'w') as summary_file:
        summary_file.write(summary)

    print(summary)




if __name__ == '__main__':

    #generating the summary of a single file
    generate_summary("test_chat.txt") 

    #generating the summary of multiple files in a folder
    generate_summary_form_multiple_files("test_folder") 
