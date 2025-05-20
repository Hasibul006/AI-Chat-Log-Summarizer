import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import string

def parsing_Messages(file_path):
    users_message = []
    ai_messages = []

    with open(file_path, 'r') as chats:
        for line in chats:
            if line.startswith('User: '):
                users_message.append(line[6:].strip())
            elif line.startswith('AI: '):
                ai_messages.append(line[4:].strip())

    return users_message, ai_messages



def avoiding_stopwords_punctuations(text):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text.lower())
    filtered_tokens = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            filtered_tokens.append(token)

    return filtered_tokens


def get_top_keywords(messages, top_n=5):

    vectorizer = TfidfVectorizer(
        tokenizer=avoiding_stopwords_punctuations,
        lowercase=True
    )

    tfidf_matrix = vectorizer.fit_transform(messages)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    word_scores = dict(zip(feature_names, scores))

    top_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    return top_keywords[:top_n]



def get_common_words(messages, top_n=5):
    stop_words = set(stopwords.words('english'))
    words = []

    for msg in messages:
        tokens = word_tokenize(msg.lower())
        for word in tokens:
            if word.isalpha() and word not in stop_words:
                words.append(word)

    word_counts = Counter(words)
    return word_counts.most_common(top_n)



def generate_summary(filepath):
    if not os.path.exists(filepath):
        print(f"File '{filepath}' not found.")
        return

    users_message, ai_messages = parsing_Messages(filepath)
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages

    common_words = get_top_keywords(users_message + ai_messages)
    #common_words = get_common_words(users_message + ai_messages)

    topics = [word for word, _ in common_words[:3]]

    summary = f"""Summary of a single file:
    - The conversation had {num_total_messages} exchanges.
    - The user asked mainly about {', '.join(topics[:3])}.
    - Most common keywords: {', '.join(topics)}.
    """
    
    print(summary)


def generate_summary_form_multiple_files(folder_path):

    users_message = []
    ai_messages = []

    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            filepath = os.path.join(folder_path, filename)
            users, ai = parsing_Messages(filepath)
            users_message.extend(users)
            ai_messages.extend(ai)
    
    num_user_messages = len(users_message)
    num_ai_messages = len(ai_messages)
    num_total_messages = num_user_messages + num_ai_messages

    common_words = get_top_keywords(users_message + ai_messages)

    topics = [word for word, _ in common_words[:3]]

    summary = f"""This the summary of multiple files:
    - The conversation had {num_total_messages} exchanges.
    - The user asked mainly about {', '.join(topics[:3])}.
    - Most common keywords: {', '.join(topics)}.
    """

    print(summary)




if __name__ == '__main__':
    generate_summary("test_chat.txt")
    generate_summary_form_multiple_files("test_folder")
